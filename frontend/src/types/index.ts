export interface Patient {
  id: number
  name: string
  age: number
  gender: string
  diabetes_type: string
  diagnosis_date: string | null
  height: number | null
  weight: number | null
  phone: string | null
  bmi?: number
  bmi_status?: string
  created_at: string
  updated_at?: string
}

export interface BloodSugar {
  id: number
  patient_id: number
  value: number
  measure_type: string
  measured_at: string
  note?: string | null
  status?: string
}

export interface BloodSugarStats {
  avg: number
  min: number
  max: number
  std: number
  count: number
  high_count: number
  low_count: number
  normal_count: number
  time_in_range: number
  trend?: string
  risk_level?: string
  error?: string
}

export interface DietRecord {
  id: number
  patient_id: number
  food_name: string
  calories: number | null
  carbs: number | null
  protein: number | null
  fat: number | null
  gi_value: number | null
  gi_level?: string
  portion: number | null
  meal_type: string | null
  eaten_at: string
}

export interface Medication {
  id: number
  patient_id: number
  drug_name: string
  drug_type: string | null
  dosage: string
  frequency: string | null
  timing: string | null
  start_date: string
  is_active: boolean
}

export interface Exercise {
  id: number
  patient_id: number
  exercise_type: string
  duration_min: number
  intensity: string
  calories_burned: number | null
  performed_at: string
  blood_sugar_before?: number | null
  blood_sugar_after?: number | null
  bs_change?: number
}

export interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface HealthReport {
  id: number
  patient_id: number
  report_type: string
  period_start: string
  period_end: string
  avg_blood_sugar: number | null
  time_in_range: number | null
  summary: string
  recommendations: string | null
  risk_level: string | null
  generated_at: string
}
