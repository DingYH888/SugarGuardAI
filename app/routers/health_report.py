"""健康报告 API 路由。"""
from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.models import Patient, HealthReport, blood_sugar, patient
from app.schemas.health_report import HealthReportResponse
from app.core.health_analyzer import health_analyzer
from app.core.llm_client import llm_client

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/generate/{patient_id}",response_model=HealthReportResponse)
async def generate_report(patient_id:int,report_type:str=Query(default="周报")):
  """ 生成健康报告 """
  # 验证患者身份
  patient = await Patient.get_or_none(id = patient_id)
  if not patient:
    raise HTTPException(status_code=404,detail="患者不存在")

  # 确定统计周期
  days = 7 if report_type == "周报" else 30 if report_type == "月报" else 0
  
  # 血糖分析
  analysis = await health_analyzer.analyze_blood_sugar(patient_id,days)
  # 生成摘要
  summary = health_analyzer.generate_summary(analysis)
  # 将统计摘要发送给LLM，获取专家建议
  if analysis.get('error'):
    recommondations = "血糖数据不足，无法生成报告。"
  else:
    # 构建提示词  
    prompt = f"请根据以下{report_type}数据生成健康建议：\n{summary}\n\n请给出3-5条具体建议。"
    # 发送提示词给LLM，获取专家建议
    recommondations = llm_client.chat(
      system_prompt="你是糖尿病健康管理专家，请给出简洁实用的健康建议。",
      user_message=prompt
     )

  # 生成报告
  report = await HealthReport.create(
    patient_id=patient_id,
    report_type = report_type,
    period_start = date.today() - timedelta(days=days),
    period_end = date.today(),
    avg_blood_sugar = analysis.get('avg',0),
    blood_sugar_std = analysis.get('std',0),
    time_in_range = analysis.get('time_in_range',0),
    summary = summary,
    recommendations = recommondations,
    risk_level = analysis.get('risk_level') or "低风险",
   )

  # 关联患者
  await report.fetch_related("patient")

  return HealthReportResponse(
    id=report.id,
    patient=patient_id,
    report_type=report.report_type,
    period_start=report.period_start,
    period_end=report.period_end,
    avg_blood_sugar=report.avg_blood_sugar,
    blood_sugar_std=report.blood_sugar_std,
    time_in_range=report.time_in_range,
    summary=report.summary,
    recommendations=report.recommendations,
    risk_level=report.risk_level,
    generated_at=report.generated_at,
   )

# 查询患者历史健康报告
@router.get("/patient/{patient_id}",response_model=List[HealthReportResponse])
async def get_reports(patient_id:int , limit:int = Query(default=10,le = 50)):
  patient = await Patient.get_or_none(id = patient_id)
  if not patient:
    raise HTTPException(status_code=404,detail="患者不存在")

  reports = await HealthReport.filter(patient_id = patient_id).order_by("-generated_at").limit(limit)
  
  return [
    HealthReportResponse(
      id=report.id,
      patient=patient_id,
      report_type=report.report_type,
      period_start=report.period_start,
      period_end=report.period_end,
      avg_blood_sugar=report.avg_blood_sugar,
      blood_sugar_std=report.blood_sugar_std,
      time_in_range=report.time_in_range,
      summary=report.summary,
      recommendations=report.recommendations,
      risk_level=report.risk_level,
      generated_at=report.generated_at,
     ) 
    for report in reports
   ]
