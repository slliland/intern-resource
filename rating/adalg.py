import pymysql
import numpy as np

# 打开数据库连接
connection = pymysql.connect(host='rm-2zeb2tu3gvi73z0opwo.mysql.rds.aliyuncs.com',
                       port=3306,
                       user='creative_brain',
                       password='cloudxink@aRdJk71X',
                       database='creative_quick_test',
                       charset='utf8mb4')

# 预估的理论最高得分，可以根据开放题类型的不同进行更改
try:
    # rsrc_ID
    rsrc_ids_input = input("输入rsrc_id（多个ID请用空格分隔）：")
    rsrc_ids = rsrc_ids_input.split()  # 拆分用户输入的ID
    rsrc_ids_formatted = ','.join(f'"{id}"' for id in rsrc_ids)  # 格式化rsrc ID

    with connection.cursor() as cursor:
        """
        统计输入rsrc ID对应的评论条数
        """
        total_num_sql = "SELECT COUNT(DISTINCT user_id) AS unique_user_count FROM cqt_survey_data WHERE rsrc_id IN ({})".format(rsrc_ids_formatted)
        cursor.execute(total_num_sql)
        result = cursor.fetchone()

        # 输出结果
        unique_user_count = result[0]
        # print("评论条数：", unique_user_count)
        '''
        查询表达5分回答的用户，记录用户ID
        查询条件与开放题选项有关，筛选好感变化/购买意向两个题目中分数最高的
        '''
        # 执行查询
        search_top_user_sql = """
                    SELECT DISTINCT user_id 
                    FROM cqt_survey_data 
                    WHERE ((topic = '好感变化' AND answer = '一定会大幅提升') 
                    OR (topic = '购买意向' AND answer = '一定会购买 ')) 
                    AND rsrc_id IN ({})""".format(rsrc_ids_formatted)
        # 若用户对两个维度都看重
        # search_top_user_sql = """
        #                     SELECT DISTINCT user_id
        #                     FROM cqt_survey_data
        #                     WHERE user_id IN (
        #                         SELECT user_id
        #                         FROM cqt_survey_data
        #                         WHERE (topic = '好感变化' AND answer = '一定会大幅提升')
        #                     ) AND user_id IN (
        #                         SELECT user_id
        #                         FROM cqt_survey_data
        #                         WHERE (topic = '购买意向' AND answer = '一定会购买 ')
        #                     ) AND rsrc_id IN ({})""".format(rsrc_ids_formatted)
        cursor.execute(search_top_user_sql)
        # 获取所有满足条件的行
        top_users = cursor.fetchall()

        # 使用集合存储唯一的user_id
        unique_user_ids = set()
        for row in top_users:
            unique_user_ids.add(row[0])  # 通过索引访问user_id

        # 表达强烈好感的5分用户评论的ID存入user_ids列表
        user_ids = []
        for user_id in unique_user_ids:
            user_ids.append(user_id)
        # 输出结果
        # print(user_ids)

        """
        5分用户评论的分维度统计，根据提及数量对维度进行权重分配
        """
        # 执行查询，获取所有维度
        dimension_sql = """
                 SELECT DISTINCT dimension_name FROM cqt_affective_disposition_result 
                 WHERE rsrc_id IN ({})
                 """.format(rsrc_ids_formatted)
        cursor.execute(dimension_sql)
        dimensions = cursor.fetchall()
        all_dimensions = [row[0] for row in dimensions]

        # 初始化维度计数字典
        dimension_counts = {dimension: 0 for dimension in all_dimensions}

        # 执行查询，获取5分用户的维度计数值，并将其累加到维度计数字典中
        for user_id in user_ids:
            user_dimension_sql = """
                     SELECT dimension_name, COUNT(*) as count
                     FROM cqt_affective_disposition_result
                     WHERE user_id = %s AND dimension_text != '无'
                     AND rsrc_id IN ({})
                     GROUP BY dimension_name
                 """.format(rsrc_ids_formatted)
            cursor.execute(user_dimension_sql, (user_id,))
            user_dimensions = cursor.fetchall()

            # 累加维度计数字典
            for dimension, count in user_dimensions:
                dimension_counts[dimension] += count

        # 输出结果
        # for dimension, count in dimension_counts.items():
        #     print(f"{dimension}: {count}")
        # 计算四分位数
        counts = list(dimension_counts.values())
        q1 = np.percentile(counts, 25)
        q2 = np.percentile(counts, 50)
        q3 = np.percentile(counts, 75)


        # 根据四分位数对用户维度分为四组
        def assign_group(count):
            if count <= q1:
                return 0
            elif q1 < count <= q2:
                return 1
            elif q2 < count <= q3:
                return 2
            else:
                return 3


        # 将维度分组存入字典
        grouped_dimensions = {dimension: assign_group(count) for dimension, count in dimension_counts.items()}

        # 输出结果
        # print("四分位数权重:")
        # for dimension, group in grouped_dimensions.items():
        #     print(f"{dimension}: {group}")

        """
        将维度权重存入cqt_affective_disposition_result表中的weight列中
        """
        # 更新维度的权重
        update_weight_sql = """
                   UPDATE cqt_affective_disposition_result
                   SET weight = %s
                   WHERE dimension_name = %s
                   AND rsrc_id IN ({})""".format(rsrc_ids_formatted)
        for dimension, group in grouped_dimensions.items():
            weight = group  # 使用分组作为权重
            cursor.execute(update_weight_sql, (weight, dimension))

        # 提交事务
        connection.commit()

        """
        用户情感权重的分维度统计，计算总分
        """
        affective_disposition_sql = """
                    SELECT dimension_name, affective_disposition_value, COUNT(*) as count
                    FROM cqt_affective_disposition_result
                    WHERE dimension_name IS NOT NULL AND affective_disposition_value IS NOT NULL
                    AND rsrc_id IN ({})
                    GROUP BY dimension_name, affective_disposition_value;
                """.format(rsrc_ids_formatted)
        cursor.execute(affective_disposition_sql)
        affective_results = cursor.fetchall()

        # 初始化维度计数字典
        affective_dimension_counts = {}

        # 遍历结果集
        for row in affective_results:
            dimension_name = row[0]
            affective_disposition_value = row[1]
            count = row[2]

            # 如果维度名称不在字典中，则初始化计数值为 0
            if dimension_name not in affective_dimension_counts:
                affective_dimension_counts[dimension_name] = {'1': 0, '0': 0, '-1': 0}

            # 将每种 affective_disposition_value 的计数值加权累加到字典中
            affective_dimension_counts[dimension_name][affective_disposition_value] += count

        # 计算加权求和并存储结果
        weighted_sums = {}
        for dimension_name, counts in affective_dimension_counts.items():
            weighted_sum = (int(counts['1']) * 1) + (int(counts['0']) * 0) + (int(counts['-1']) * -1)
            weighted_sums[dimension_name] = weighted_sum

        # 输出结果
        # for dimension_name, weighted_sum in weighted_sums.items():
        #     print(f"{dimension_name}: {weighted_sum}")

        # 将affective求和与权重相乘
        final_scores = {dimension: weighted_sums[dimension] * grouped_dimensions[dimension] for dimension in
                        all_dimensions}

        # 输出结果
        # for dimension, score in final_scores.items():
        #     print(f"{dimension}: {score}")

        # 计算所有维度的总分
        total_score = sum(final_scores.values())

        """
        输出最终计算出的分数结果：
        原始得分为实际计算出的总分
        最终得分为将原始得分映射到50-150范围内的得分
        """
        def tanh_stretch(x, stretch_factor=1):
            # 双曲正切函数进行非线性拉伸
            return np.tanh(x * stretch_factor)


        # 根据数据分布情况可以修改 non_linear_param 的值
        def nonlinear_to_linear_mapping(value, old_min, old_max, new_min, new_max, non_linear_func, non_linear_param):
            # 将原始值归一化到[0,1]区间
            normalized_value = (value - old_min) / (old_max - old_min)
            # 应用非线性拉伸函数
            value_nonlinear_mapped = non_linear_func(normalized_value, non_linear_param)
            # 线性映射到新的范围
            value_linear_mapped = new_min + (new_max - new_min) * value_nonlinear_mapped
            return value_linear_mapped


        # 估计的数据最小值和最大值
        estimated_old_min, estimated_old_max = 0, 3000

        # 映射范围
        new_min, new_max = 50, 150

        # 使用tanh函数拉伸
        mapped_value = nonlinear_to_linear_mapping(total_score, estimated_old_min, estimated_old_max, new_min, new_max,
                                                   tanh_stretch, 1.5)
        final_score = np.round(mapped_value, 0)

        print(f"原始得分: {total_score}")
        print(f"最终得分: {final_score}")

finally:
    # 关闭连接
    connection.close()