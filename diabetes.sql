/*
 Navicat MySQL Data Transfer

 Source Server         : AI健康助手
 Source Server Type    : MySQL
 Source Server Version : 80012 (8.0.12)
 Source Host           : localhost:3306
 Source Schema         : diabetes

 Target Server Type    : MySQL
 Target Server Version : 80012 (8.0.12)
 File Encoding         : 65001

 Date: 02/07/2026 10:49:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for blood_sugar
-- ----------------------------
DROP TABLE IF EXISTS `blood_sugar`;
CREATE TABLE `blood_sugar`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) NOT NULL,
  `value` float NOT NULL,
  `measure_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `measured_at` datetime NOT NULL,
  `note` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patient_id`(`patient_id` ASC) USING BTREE,
  CONSTRAINT `blood_sugar_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blood_sugar
-- ----------------------------
INSERT INTO `blood_sugar` VALUES (1, 1, 6.8, '空腹', '2026-04-01 07:00:00', '晨起空腹', '2026-06-08 11:35:25');
INSERT INTO `blood_sugar` VALUES (2, 1, 9.2, '餐后2h', '2026-04-01 09:30:00', '早餐后', '2026-06-08 11:35:25');
INSERT INTO `blood_sugar` VALUES (3, 1, 6.5, '空腹', '2026-04-02 07:00:00', '', '2026-06-08 11:35:25');
INSERT INTO `blood_sugar` VALUES (4, 1, 8.8, '餐后2h', '2026-04-02 09:30:00', '杂粮馒头', '2026-06-08 11:35:25');
INSERT INTO `blood_sugar` VALUES (5, 1, 7.1, '空腹', '2026-04-03 07:00:00', '', '2026-06-08 11:35:25');
INSERT INTO `blood_sugar` VALUES (6, 1, 10.5, '餐后2h', '2026-04-03 12:30:00', '米饭较多', '2026-06-08 11:35:25');
INSERT INTO `blood_sugar` VALUES (7, 1, 5.9, '空腹', '2026-04-04 07:00:00', '', '2026-06-08 11:35:25');
INSERT INTO `blood_sugar` VALUES (8, 1, 8.2, '餐后2h', '2026-04-04 12:30:00', '', '2026-06-08 11:35:25');
INSERT INTO `blood_sugar` VALUES (9, 1, 6.3, '睡前', '2026-04-04 22:00:00', '', '2026-06-08 11:35:25');
INSERT INTO `blood_sugar` VALUES (10, 1, 6.2, '空腹', '2026-04-05 07:00:00', '控制不错', '2026-06-08 11:35:25');
INSERT INTO `blood_sugar` VALUES (12, 1, 6.4, '餐后2h', '2026-06-25 03:08:49', NULL, '2026-06-10 03:09:00');
INSERT INTO `blood_sugar` VALUES (13, 1, 8.5, '空腹', '2026-06-30 07:37:15', NULL, '2026-06-16 07:37:30');
INSERT INTO `blood_sugar` VALUES (14, 1, 5.6, '空腹', '2026-06-30 07:49:43', NULL, '2026-06-16 07:49:57');
INSERT INTO `blood_sugar` VALUES (15, 1, 6, '空腹', '2026-06-23 02:16:46', NULL, '2026-06-23 02:16:55');

-- ----------------------------
-- Table structure for chat_history
-- ----------------------------
DROP TABLE IF EXISTS `chat_history`;
CREATE TABLE `chat_history`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) NOT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patient_id`(`patient_id` ASC) USING BTREE,
  CONSTRAINT `chat_history_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 50 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chat_history
-- ----------------------------
INSERT INTO `chat_history` VALUES (46, 1, 'user', '我今天血糖偏高怎么办', '2026-07-01 09:20:32');
INSERT INTO `chat_history` VALUES (47, 1, 'assistant', '张先生，您好！看到您说今天血糖偏高，请先别太着急。从您近7天的记录来看，您的平均血糖是6.8 mmol/L，达标率高达100%，这说明您近期的整体血糖管理得非常棒！偶尔一次的血糖波动是很正常的，咱们来一步步应对。\n\n### 一、 对您当前状况的分析\n1. **确认是否真的“偏高”**：根据医学指南，空腹血糖控制在 **4.4-7.0 mmol/L**，餐后2小时血糖 **<10.0 mmol/L** 都属于达标。您可以对照一下，今天的数值是否其实还在安全范围内？\n2. **寻找波动原因**：偶尔一次偏高，通常与昨晚睡眠质量不佳、某一餐主食或油脂吃得稍多、情绪波动、或是运动量比平时少有关，不必过度焦虑。\n\n### 二、 具体可执行的建议\n1. **多喝温水**：在心脏和肾功能允许的情况下，适当多喝点白开水，有助于稀释血液，促进糖分通过尿液排出。\n2. **适度活动**：如果当前血糖没有超过 16.7 mmol/L，且身体没有头晕、乏力等不适，建议去散步或做点轻松的家务 20-30 分钟，能有效帮助肌肉消耗掉多余的血糖。\n3. **调整下一餐饮食**：下一顿饭适当减少主食（如米、面）的量，可以换成粗粮；多吃绿叶蔬菜，搭配适量的优质蛋白（如瘦肉、鱼虾或豆腐），做到清淡少油。\n\n### 三、 需要注意的事项\n1. **切勿自行加药**：千万不要因为一次血糖偏高就自行增加降糖药的剂量，以免引发低血糖（血糖 <3.9 mmol/L 非常危险）。\n2. **关注体重与心血管健康**：您的 BMI 为 26.4，体重偏胖，且伴有高血压和血脂偏高。建议日常饮食务必做到 **“低盐、低脂、低糖”**。在身体允许的情况下，坚持规律的有氧运动，循序渐进地减轻体重，这对同时改善血糖、血压和血脂有极大的帮助。\n3. **持续监测**：请继续按常规监测明天的空腹和餐后血糖。如果连续两三天血糖都持续偏高，请及时复诊，由医生来评估是否需要调整治疗方案。\n\n您近期的整体控制得非常出色，请继续保持信心！如果方便的话，您可以告诉我今天具体的**血糖数值**以及是**空腹还是餐后**测量的，我再帮您做更针对性的分析。祝您今天心情愉快，身体健康！', '2026-07-01 09:21:02');
INSERT INTO `chat_history` VALUES (48, 1, 'user', '我今天适合吃什么食物', '2026-07-01 09:21:22');
INSERT INTO `chat_history` VALUES (49, 1, 'assistant', '张先生您好！看到您近7天的血糖平均值在6.8 mmol/L，达标率100%且趋势稳定，这说明您近期的自我管理非常棒，请继续保持！\n\n**【当前状况分析】**\n您的血糖目前控制得很理想，但考虑到您的BMI为26.4（属于超重），且伴有5年高血压和血脂偏高，我们在保持血糖稳定的同时，饮食的核心目标应放在**控制总热量（帮助减重）、低盐低脂（保护心血管）** 以及**维持低GI（升糖指数）饮食**上。\n\n**【今日具体饮食建议】**\n结合您的身体情况，今天为您推荐以下低GI、高纤维且对心血管友好的食物搭配：\n\n*   **主食类（优选低GI，增加饱腹感）**\n    *   **推荐吃**：燕麦、糙米或蒸红薯。建议把日常的白米饭换成“糙米燕麦饭”或者杂粮饭，富含膳食纤维，升糖慢。\n    *   **尽量不吃**：白米饭、白面条、白面包、糯米和土豆泥，这些食物升糖速度太快。\n*   **肉蛋奶类（优选低脂优质蛋白）**\n    *   **推荐吃**：清蒸鱼、去皮禽肉（如鸡胸肉）、豆腐或水煮蛋。特别是深海鱼或淡水鱼，富含不饱和脂肪酸，对改善您的血脂非常有帮助。\n    *   **尽量不吃**：肥肉、动物内脏、加工肉制品（如香肠、培根），以免加重血脂负担。\n*   **蔬菜类（补充膳食纤维，每天需25-30g）**\n    *   **推荐吃**：西兰花、芹菜、菠菜、木耳、海带等。尤其是芹菜和木耳，对高血压和高血脂患者非常友好。建议每餐蔬菜的量占到餐盘的一半。\n*   **水果与加餐（解馋且升糖慢）**\n    *   **推荐吃**：苹果或梨。建议放在两餐之间（如上午10点或下午3点）吃半个（约100-150克），不要饭后马上吃。\n    *   **尽量不吃**：西瓜等高GI水果。\n\n**【需要特别注意的事项】**\n1.  **清淡烹饪**：因为您有高血压和血脂偏高，做菜时请务必**少盐少油**（每天食盐不超过5克，约一平啤酒瓶盖），多用蒸、煮、凉拌、清炒的方式。\n2.  **调整进餐顺序**：建议按照 **“先吃蔬菜 -> 再吃肉/蛋 -> 最后吃主食”** 的顺序进餐。这个小习惯能像“海绵”一样延缓碳水化合物的吸收，让餐后血糖更平稳。\n3.  **吃动平衡**：您目前体重偏胖，建议在三餐后半小时，进行30分钟左右的中等强度运动（如快走、打太极），既能帮助消耗热量、减轻体重，又能辅助降压和降糖。\n\n祝您今天用餐愉快，身体越来越健康！如果有任何饮食上的疑问，随时可以问我。', '2026-07-01 09:21:53');

-- ----------------------------
-- Table structure for diet_records
-- ----------------------------
DROP TABLE IF EXISTS `diet_records`;
CREATE TABLE `diet_records`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) NOT NULL,
  `food_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `calories` float NULL DEFAULT NULL,
  `carbs` float NULL DEFAULT NULL,
  `protein` float NULL DEFAULT NULL,
  `fat` float NULL DEFAULT NULL,
  `gi_value` float NULL DEFAULT NULL,
  `portion` float NULL DEFAULT 1,
  `meal_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `eaten_at` datetime NOT NULL,
  `note` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patient_id`(`patient_id` ASC) USING BTREE,
  CONSTRAINT `diet_records_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of diet_records
-- ----------------------------
INSERT INTO `diet_records` VALUES (1, 1, '燕麦粥', 150, 27, 5, 3, 55, 1, '早餐', '2026-04-01 07:30:00', NULL, '2026-06-08 11:35:25');
INSERT INTO `diet_records` VALUES (2, 1, '水煮鸡蛋', 78, 0.6, 6, 5, 0, 1, '早餐', '2026-04-01 07:30:00', NULL, '2026-06-08 11:35:25');
INSERT INTO `diet_records` VALUES (3, 1, '清炒西兰花', 55, 6, 4, 2, 15, 1, '午餐', '2026-04-01 12:00:00', NULL, '2026-06-08 11:35:25');
INSERT INTO `diet_records` VALUES (4, 1, '糙米饭', 220, 46, 5, 2, 56, 1, '午餐', '2026-04-01 12:00:00', NULL, '2026-06-08 11:35:25');
INSERT INTO `diet_records` VALUES (5, 1, '红烧豆腐', 120, 5, 12, 6, 15, 1, '午餐', '2026-04-01 12:00:00', NULL, '2026-06-08 11:35:25');
INSERT INTO `diet_records` VALUES (8, 1, '米饭', 10, 10, 10, 10, 10, 1, '早餐', '2026-06-15 00:00:00', NULL, '2026-06-15 03:17:56');
INSERT INTO `diet_records` VALUES (9, 1, '辣椒炒肉', 20, 20, 20, 20, 4, 1, '午餐', '2026-06-15 00:00:00', NULL, '2026-06-15 03:35:30');
INSERT INTO `diet_records` VALUES (10, 1, '鸡蛋', 10, 10, 10, 10, 10, 1, '早餐', '2026-06-24 07:00:00', NULL, '2026-06-23 02:18:41');

-- ----------------------------
-- Table structure for exercise_records
-- ----------------------------
DROP TABLE IF EXISTS `exercise_records`;
CREATE TABLE `exercise_records`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) NOT NULL,
  `exercise_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `duration_min` int(11) NOT NULL,
  `intensity` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '中等',
  `calories_burned` float NULL DEFAULT NULL,
  `performed_at` datetime NOT NULL,
  `blood_sugar_before` float NULL DEFAULT NULL,
  `blood_sugar_after` float NULL DEFAULT NULL,
  `note` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patient_id`(`patient_id` ASC) USING BTREE,
  CONSTRAINT `exercise_records_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of exercise_records
-- ----------------------------
INSERT INTO `exercise_records` VALUES (1, 1, '快走', 30, '中等', 150, '2026-04-01 18:00:00', 8.5, 6.8, NULL, '2026-06-08 11:35:25');
INSERT INTO `exercise_records` VALUES (2, 1, '太极拳', 45, '低', 120, '2026-04-02 06:30:00', 6.5, 5.8, NULL, '2026-06-08 11:35:25');
INSERT INTO `exercise_records` VALUES (3, 1, '骑自行车', 40, '中等', 200, '2026-04-03 17:30:00', 9, 7.2, NULL, '2026-06-08 11:35:25');
INSERT INTO `exercise_records` VALUES (4, 2, '瑜伽', 60, '低', 180, '2026-04-01 09:00:00', 7, 6.2, NULL, '2026-06-08 11:35:25');

-- ----------------------------
-- Table structure for health_reports
-- ----------------------------
DROP TABLE IF EXISTS `health_reports`;
CREATE TABLE `health_reports`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) NOT NULL,
  `report_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `period_start` date NOT NULL,
  `period_end` date NOT NULL,
  `avg_blood_sugar` float NULL DEFAULT NULL,
  `blood_sugar_std` float NULL DEFAULT NULL,
  `time_in_range` float NULL DEFAULT NULL,
  `summary` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `recommendations` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `risk_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '低',
  `generated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patient_id`(`patient_id` ASC) USING BTREE,
  CONSTRAINT `health_reports_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of health_reports
-- ----------------------------
INSERT INTO `health_reports` VALUES (11, 1, '周报', '2026-06-15', '2026-06-22', 6.8, 1.5, 100, '近7天血糖概况：共记录3次，平均值6.8 mmol/L，范围5.6-8.5 mmol/L。达标率100.0%，趋势稳定。', '根据您的周报数据，您的血糖控制非常理想，趋势稳定且100%达标。以下是为您提供的4条简洁实用的健康建议：\n\n1. **保持当前良好习惯**：您的平均血糖（6.8 mmol/L）和波动范围都非常优秀，请继续保持现有的饮食、运动和用药方案，切勿因血糖达标而自行减药或停药。\n2. **适当增加监测频次**：近7天仅记录3次偏少。建议每周至少挑2-3天，进行“空腹+餐后2小时”的配对监测，以便更全面地掌握全天的血糖波动情况。\n3. **关注最高值来源**：您的最高值为8.5 mmol/L，大概率出现在餐后。建议留意餐后血糖，若某餐后偏高，可复盘当餐饮食，找出容易引起血糖波动的特定食物并加以调整。\n4. **定期复查糖化血红蛋白**：日常指尖血糖达标是好事，但建议每3-6个月去医院复查一次糖化血红蛋白（HbA1c）以评估长期血糖水平，并遵医嘱进行年度并发症筛查。', '低风险', '2026-06-22 08:01:15');

-- ----------------------------
-- Table structure for medications
-- ----------------------------
DROP TABLE IF EXISTS `medications`;
CREATE TABLE `medications`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) NOT NULL,
  `drug_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `drug_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `dosage` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `frequency` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `timing` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `start_date` date NOT NULL,
  `end_date` date NULL DEFAULT NULL,
  `is_active` tinyint(1) NULL DEFAULT 1,
  `side_effects` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `note` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patient_id`(`patient_id` ASC) USING BTREE,
  CONSTRAINT `medications_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of medications
-- ----------------------------
INSERT INTO `medications` VALUES (1, 1, '二甲双胍', '口服药', '500mg', '每日2次', '餐后服用', '2020-04-01', NULL, 1, NULL, NULL, '2026-06-08 11:35:25');
INSERT INTO `medications` VALUES (2, 1, '格列美脲', '口服药', '2mg', '每日1次', '早餐前30分钟', '2021-06-15', NULL, 1, NULL, NULL, '2026-06-08 11:35:25');
INSERT INTO `medications` VALUES (3, 1, '阿托伐他汀', '口服药', '20mg', '每日1次', '睡前', '2020-05-01', NULL, 1, NULL, NULL, '2026-06-08 11:35:25');
INSERT INTO `medications` VALUES (4, 2, '二甲双胍', '口服药', '850mg', '每日2次', '餐后', '2022-09-01', NULL, 1, NULL, NULL, '2026-06-08 11:35:25');
INSERT INTO `medications` VALUES (5, 4, '门冬胰岛素', '胰岛素', '按需', '每日3次', '餐前', '2015-07-01', NULL, 1, NULL, NULL, '2026-06-08 11:35:25');
INSERT INTO `medications` VALUES (6, 4, '甘精胰岛素', '胰岛素', '18U', '每日1次', '睡前', '2015-07-01', NULL, 1, NULL, NULL, '2026-06-08 11:35:25');

-- ----------------------------
-- Table structure for patients
-- ----------------------------
DROP TABLE IF EXISTS `patients`;
CREATE TABLE `patients`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `age` int(11) NOT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '未知',
  `diabetes_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '2型',
  `diagnosis_date` date NULL DEFAULT NULL,
  `height` float NULL DEFAULT NULL,
  `weight` float NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `emergency_contact` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `emergency_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `medical_history` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `allergies` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of patients
-- ----------------------------
INSERT INTO `patients` VALUES (1, '张伟', 55, '男', '2型', '2020-03-15', 172, 78, '13800138001', NULL, NULL, '高血压5年，血脂偏高', NULL, '2026-06-08 11:35:25', '2026-06-08 11:35:25');
INSERT INTO `patients` VALUES (2, '李芳', 42, '女', '2型', '2022-08-20', 160, 62, '13800138002', NULL, NULL, '无其他慢性病', NULL, '2026-06-08 11:35:25', '2026-06-08 11:35:25');
INSERT INTO `patients` VALUES (3, '王强', 68, '男', '2型', '2018-01-10', 170, 82, '13800138003', NULL, NULL, '冠心病，糖尿病肾病早期', NULL, '2026-06-08 11:35:25', '2026-06-08 11:35:25');
INSERT INTO `patients` VALUES (4, '赵敏', 35, '女', '1型', '2015-06-05', 165, 55, '13800138004', NULL, NULL, '1型糖尿病，使用胰岛素泵', NULL, '2026-06-08 11:35:25', '2026-06-08 11:35:25');
INSERT INTO `patients` VALUES (5, '陈刚', 50, '男', '2型', '2021-11-30', 178, 90, '13800138005', NULL, NULL, '肥胖，脂肪肝', NULL, '2026-06-08 11:35:25', '2026-06-08 11:35:25');

SET FOREIGN_KEY_CHECKS = 1;
