import datetime
import requests

CONN = '172.105.37.122:32149'
DB_NAME = 'test'
TABLE_NAME = 'rand_data2'
NUM_ROWS = 100000000


EXPECT_RESULTS = {
    1000000: {
        'insert_time': datetime.timedelta(seconds=90),
        'increments_per_hour': {
            1: [{'min_ts': '2022-08-27 15:50:12.577987', 'max_ts': '2022-08-27 15:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2026798154079276, 'row_count': 6799},
                {'min_ts': '2022-08-27 16:00:00.011587', 'max_ts': '2022-08-27 16:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024459856932978, 'row_count': 41667},
                {'min_ts': '2022-08-27 17:00:00.040387', 'max_ts': '2022-08-27 17:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20252618035537587, 'row_count': 41667},
                {'min_ts': '2022-08-27 18:00:00.069187', 'max_ts': '2022-08-27 18:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024355324958677, 'row_count': 41666},
                {'min_ts': '2022-08-27 19:00:00.011587', 'max_ts': '2022-08-27 19:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247818073937282, 'row_count': 41667},
                {'min_ts': '2022-08-27 20:00:00.040387', 'max_ts': '2022-08-27 20:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024853993793405, 'row_count': 41667},
                {'min_ts': '2022-08-27 21:00:00.069187', 'max_ts': '2022-08-27 21:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2025518260037256, 'row_count': 41666},
                {'min_ts': '2022-08-27 22:00:00.011587', 'max_ts': '2022-08-27 22:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20253437559344936, 'row_count': 41667},
                {'min_ts': '2022-08-27 23:00:00.040387', 'max_ts': '2022-08-27 23:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247503709299325, 'row_count': 41667},
                {'min_ts': '2022-08-28 00:00:00.069187', 'max_ts': '2022-08-28 00:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.202455896187629, 'row_count': 41666},
                {'min_ts': '2022-08-28 01:00:00.011587', 'max_ts': '2022-08-28 01:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024459856932978, 'row_count': 41667},
                {'min_ts': '2022-08-28 02:00:00.040387', 'max_ts': '2022-08-28 02:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20252618035537587, 'row_count': 41667},
                {'min_ts': '2022-08-28 03:00:00.069187', 'max_ts': '2022-08-28 03:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024355324958677, 'row_count': 41666},
                {'min_ts': '2022-08-28 04:00:00.011587', 'max_ts': '2022-08-28 04:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247818073937282, 'row_count': 41667},
                {'min_ts': '2022-08-28 05:00:00.040387', 'max_ts': '2022-08-28 05:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024853993793405, 'row_count': 41667},
                {'min_ts': '2022-08-28 06:00:00.069187', 'max_ts': '2022-08-28 06:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2025518260037256, 'row_count': 41666},
                {'min_ts': '2022-08-28 07:00:00.011587', 'max_ts': '2022-08-28 07:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20253437559344936, 'row_count': 41667},
                {'min_ts': '2022-08-28 08:00:00.040387', 'max_ts': '2022-08-28 08:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247503709299325, 'row_count': 41667},
                {'min_ts': '2022-08-28 09:00:00.069187', 'max_ts': '2022-08-28 09:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.202455896187629, 'row_count': 41666},
                {'min_ts': '2022-08-28 10:00:00.011587', 'max_ts': '2022-08-28 10:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024459856932978, 'row_count': 41667},
                {'min_ts': '2022-08-28 11:00:00.040387', 'max_ts': '2022-08-28 11:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20252618035537587, 'row_count': 41667},
                {'min_ts': '2022-08-28 12:00:00.069187', 'max_ts': '2022-08-28 12:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024355324958677, 'row_count': 41666},
                {'min_ts': '2022-08-28 13:00:00.011587', 'max_ts': '2022-08-28 13:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247818073937282, 'row_count': 41667},
                {'min_ts': '2022-08-28 14:00:00.040387', 'max_ts': '2022-08-28 14:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024853993793405, 'row_count': 41667},
                {'min_ts': '2022-08-28 15:00:00.069187', 'max_ts': '2022-08-28 15:50:12.491587', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20252052188598418, 'row_count': 34867}],
            2: [{'min_ts': '2022-08-27 15:50:12.577987', 'max_ts': '2022-08-27 15:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2026798154079276, 'row_count': 6799},
                {'min_ts': '2022-08-27 16:00:00.011587', 'max_ts': '2022-08-27 17:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248608302433685, 'row_count': 83334},
                {'min_ts': '2022-08-27 18:00:00.069187', 'max_ts': '2022-08-27 19:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20245685687351073, 'row_count': 83333},
                {'min_ts': '2022-08-27 20:00:00.040387', 'max_ts': '2022-08-27 21:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20251861229297174, 'row_count': 83333},
                {'min_ts': '2022-08-27 22:00:00.011587', 'max_ts': '2022-08-27 23:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20250470634322132, 'row_count': 83334},
                {'min_ts': '2022-08-28 00:00:00.069187', 'max_ts': '2022-08-28 01:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024509408810002, 'row_count': 83333},
                {'min_ts': '2022-08-28 02:00:00.040387', 'max_ts': '2022-08-28 03:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024808569695111, 'row_count': 83333},
                {'min_ts': '2022-08-28 04:00:00.011587', 'max_ts': '2022-08-28 05:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248179005935665, 'row_count': 83334},
                {'min_ts': '2022-08-28 06:00:00.069187', 'max_ts': '2022-08-28 07:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20254310069388462, 'row_count': 83333},
                {'min_ts': '2022-08-28 08:00:00.040387', 'max_ts': '2022-08-28 09:59:59.925187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.202465466755157, 'row_count': 83333},
                {'min_ts': '2022-08-28 10:00:00.011587', 'max_ts': '2022-08-28 11:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248608302433685, 'row_count': 83334},
                {'min_ts': '2022-08-28 12:00:00.069187', 'max_ts': '2022-08-28 13:59:59.953987', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20245685687351073, 'row_count': 83333},
                {'min_ts': '2022-08-28 14:00:00.040387', 'max_ts': '2022-08-28 15:50:12.491587', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20250140032583677, 'row_count': 76534}],
            6: [{'min_ts': '2022-08-27 15:50:12.577987', 'max_ts': '2022-08-27 17:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20250069683366342, 'row_count': 90133},
                {'min_ts': '2022-08-27 18:00:00.069187', 'max_ts': '2022-08-27 23:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20249339188182597, 'row_count': 250000},
                {'min_ts': '2022-08-28 00:00:00.069187', 'max_ts': '2022-08-28 05:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247119601233238, 'row_count': 250000},
                {'min_ts': '2022-08-28 06:00:00.069187', 'max_ts': '2022-08-28 11:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20249821677592428, 'row_count': 250000},
                {'min_ts': '2022-08-28 12:00:00.069187', 'max_ts': '2022-08-28 15:50:12.491587', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247818140315302, 'row_count': 159867}],
            12: [{'min_ts': '2022-08-27 15:50:12.577987', 'max_ts': '2022-08-27 23:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024953276458476, 'row_count': 340133},
                 {'min_ts': '2022-08-28 00:00:00.069187', 'max_ts': '2022-08-28 11:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248470639412833, 'row_count': 500000},
                 {'min_ts': '2022-08-28 12:00:00.069187', 'max_ts': '2022-08-28 15:50:12.491587', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247818140315302, 'row_count': 159867}],
            24: [{'min_ts': '2022-08-27 15:50:12.577987', 'max_ts': '2022-08-27 23:59:59.982787', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024953276458476, 'row_count': 340133},
                 {'min_ts': '2022-08-28 00:00:00.069187', 'max_ts': '2022-08-28 15:50:12.491587', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248312557445974, 'row_count': 659867}]
        }
    },
    10000000: {
        'insert_time': datetime.timedelta(minutes=30),
        'increments_per_hour': {
            1: [{'min_ts': '2022-08-27 15:50:12.577987', 'max_ts': '2022-08-27 15:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247305224887488, 'row_count': 67989},
                {'min_ts': '2022-08-27 16:00:00.002947', 'max_ts': '2022-08-27 16:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248665946817906, 'row_count': 416667},
                {'min_ts': '2022-08-27 17:00:00.005827', 'max_ts': '2022-08-27 17:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248994577216065, 'row_count': 416666},
                {'min_ts': '2022-08-27 18:00:00.000067', 'max_ts': '2022-08-27 18:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20249145946433908, 'row_count': 416667},
                {'min_ts': '2022-08-27 19:00:00.002947', 'max_ts': '2022-08-27 19:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.202492278994047, 'row_count': 416667},
                {'min_ts': '2022-08-27 20:00:00.005827', 'max_ts': '2022-08-27 20:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248683106928347, 'row_count': 416666},
                {'min_ts': '2022-08-27 21:00:00.000067', 'max_ts': '2022-08-27 21:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024839451031977, 'row_count': 416667},
                {'min_ts': '2022-08-27 22:00:00.002947', 'max_ts': '2022-08-27 22:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248343994039117, 'row_count': 416667},
                {'min_ts': '2022-08-27 23:00:00.005827', 'max_ts': '2022-08-27 23:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248986698032473, 'row_count': 416666},
                {'min_ts': '2022-08-28 00:00:00.000067', 'max_ts': '2022-08-28 00:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248398722753885, 'row_count': 416667},
                {'min_ts': '2022-08-28 01:00:00.002947', 'max_ts': '2022-08-28 01:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248665946817906, 'row_count': 416667},
                {'min_ts': '2022-08-28 02:00:00.005827', 'max_ts': '2022-08-28 02:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248994577216065, 'row_count': 416666},
                {'min_ts': '2022-08-28 03:00:00.000067', 'max_ts': '2022-08-28 03:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20249145946433908, 'row_count': 416667},
                {'min_ts': '2022-08-28 04:00:00.002947', 'max_ts': '2022-08-28 04:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.202492278994047, 'row_count': 416667},
                {'min_ts': '2022-08-28 05:00:00.005827', 'max_ts': '2022-08-28 05:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248683106928347, 'row_count': 416666},
                {'min_ts': '2022-08-28 06:00:00.000067', 'max_ts': '2022-08-28 06:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024839451031977, 'row_count': 416667},
                {'min_ts': '2022-08-28 07:00:00.002947', 'max_ts': '2022-08-28 07:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248343994039117, 'row_count': 416667},
                {'min_ts': '2022-08-28 08:00:00.005827', 'max_ts': '2022-08-28 08:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248986698032473, 'row_count': 416666},
                {'min_ts': '2022-08-28 09:00:00.000067', 'max_ts': '2022-08-28 09:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248398722753885, 'row_count': 416667},
                {'min_ts': '2022-08-28 10:00:00.002947', 'max_ts': '2022-08-28 10:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248665946817906, 'row_count': 416667},
                {'min_ts': '2022-08-28 11:00:00.005827', 'max_ts': '2022-08-28 11:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248994577216065, 'row_count': 416666},
                {'min_ts': '2022-08-28 12:00:00.000067', 'max_ts': '2022-08-28 12:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20249145946433908, 'row_count': 416667},
                {'min_ts': '2022-08-28 13:00:00.002947', 'max_ts': '2022-08-28 13:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.202492278994047, 'row_count': 416667},
                {'min_ts': '2022-08-28 14:00:00.005827', 'max_ts': '2022-08-28 14:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248683106928347, 'row_count': 416666},
                {'min_ts': '2022-08-28 15:00:00.000067', 'max_ts': '2022-08-28 15:50:12.569347', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247855010931104, 'row_count': 348678}],
            2: [{'min_ts': '2022-08-27 15:50:12.577987', 'max_ts': '2022-08-27 15:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20247305224887488, 'row_count': 67989},
                {'min_ts': '2022-08-27 16:00:00.002947', 'max_ts': '2022-08-27 17:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248830261819808, 'row_count': 833333},
                {'min_ts': '2022-08-27 18:00:00.000067', 'max_ts': '2022-08-27 19:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20249186922919302, 'row_count': 833334},
                {'min_ts': '2022-08-27 20:00:00.005827', 'max_ts': '2022-08-27 21:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.202485388084509, 'row_count': 833333},
                {'min_ts': '2022-08-27 22:00:00.002947', 'max_ts': '2022-08-27 23:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248665345650174, 'row_count': 833333},
                {'min_ts': '2022-08-28 00:00:00.000067', 'max_ts': '2022-08-28 01:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248532334785896, 'row_count': 833334},
                {'min_ts': '2022-08-28 02:00:00.005827', 'max_ts': '2022-08-28 03:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20249070261915808, 'row_count': 833333},
                {'min_ts': '2022-08-28 04:00:00.002947', 'max_ts': '2022-08-28 05:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.202489555034934, 'row_count': 833333},
                {'min_ts': '2022-08-28 06:00:00.000067', 'max_ts': '2022-08-28 07:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024836925217944, 'row_count': 833334},
                {'min_ts': '2022-08-28 08:00:00.005827', 'max_ts': '2022-08-28 09:59:59.994307', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248692710040395, 'row_count': 833333},
                {'min_ts': '2022-08-28 10:00:00.002947', 'max_ts': '2022-08-28 11:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248830261819808, 'row_count': 833333},
                {'min_ts': '2022-08-28 12:00:00.000067', 'max_ts': '2022-08-28 13:59:59.997187', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20249186922919302, 'row_count': 833334},
                {'min_ts': '2022-08-28 14:00:00.005827', 'max_ts': '2022-08-28 15:50:12.569347', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248305840161868, 'row_count': 765344}],
            6: [{'min_ts': '2022-08-27 15:50:12.577987', 'max_ts': '2022-08-27 17:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248715224423636, 'row_count': 901322},
                {'min_ts': '2022-08-27 18:00:00.000067', 'max_ts': '2022-08-27 23:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248797025829418, 'row_count': 2500000},
                {'min_ts': '2022-08-28 00:00:00.000067', 'max_ts': '2022-08-28 05:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024885269993689, 'row_count': 2500000},
                {'min_ts': '2022-08-28 06:00:00.000067', 'max_ts': '2022-08-28 11:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248630741241955, 'row_count': 2500000},
                {'min_ts': '2022-08-28 12:00:00.000067', 'max_ts': '2022-08-28 15:50:12.569347', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.202487651172762, 'row_count': 1598678}],
            12: [{'min_ts': '2022-08-27 15:50:12.577987', 'max_ts': '2022-08-27 23:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248775349138218, 'row_count': 3401322},
                 {'min_ts': '2022-08-28 00:00:00.000067', 'max_ts': '2022-08-28 11:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.2024874172058942, 'row_count': 5000000},
                 {'min_ts': '2022-08-28 12:00:00.000067', 'max_ts': '2022-08-28 15:50:12.569347', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.202487651172762, 'row_count': 1598678}],
            24: [{'min_ts': '2022-08-27 15:50:12.577987', 'max_ts': '2022-08-27 23:59:59.991427', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248775349138218, 'row_count': 3401322},
                 {'min_ts': '2022-08-28 00:00:00.000067', 'max_ts': '2022-08-28 15:50:12.569347', 'min_val': -1.0, 'max_val': 1.0, 'avg_val': 0.20248747388962454, 'row_count': 6598678}]
        }
    },
    100000000: {
        'insert_time': datetime.timedelta(hours=4),
        'increments_per_hour': {
            1: []
        }
    }
}


def get_results(query:str, sql:bool=True, networking:bool=True)->list:
    """
    Get results from query
    :args:
        query:str - Query to execute
        sql:bool - whetheer this is a SQL
        networking:bool - whether to execute against network
    :params:
        output:list - output from results
        headers:list - list of headers
    :return:
        output
    """
    output = []
    headers = {
        'User-Agent': 'AnyLog/1.23'
    }
    if sql is True:
        headers['command'] = f'sql {DB_NAME} format=json and stat=false "{query}"'
    if networking is True:
        headers['destination'] =  'network'
    try:
        r = requests.get(url=f'http://{CONN}', headers=headers, timeout=90)
    except Exception as error:
        print(f'Failed to execute GET against {CONN} | Query: {query} (Error: {error})')
    else:
        if int(r.status_code) != 200:
            print(f'Failed to execute GET against {CONN} | Query: {query} (Network Error: {r.status_code})')
        else:
            try:
                output = r.json()['Query']
            except Exception as error:
                print(f'Failed to extract results (Error {error})\n\tAnyLog Error: {r.text}')
    return output


def test_row_count():
    """
    Validate all rows inserted
    :query:
        SELECT COUNT(*) FROM {TABLE_NAME}
    :assert:
        number of rows is as expected
    """
    query = f"SELECT COUNT(*) FROM {TABLE_NAME}"
    results = get_results(query=query, sql=True, networking=True)
    assert results[0]['count(*)'] == NUM_ROWS


def test_insert_time():
    """
    Validate length of time inserts took is less than (or equal to what's expected)
    :query:
        SELECT MIN(insert_timestamp) as min_ts, max(insert_timestamp) as max_ts FROM {TABLE_NAME}
    :assert:
        total amount of time inserts took
    """
    query = f"SELECT MIN(insert_timestamp) as min_ts, max(insert_timestamp) as max_ts FROM {TABLE_NAME}"
    results = get_results(query=query, sql=True, networking=True)
    min_ts = datetime.datetime.strptime(results[0]['min_ts'], '%Y-%m-%d %H:%M:%S.%f')
    max_ts = datetime.datetime.strptime(results[0]['max_ts'], '%Y-%m-%d %H:%M:%S.%f')
    assert max_ts - min_ts < EXPECT_RESULTS[NUM_ROWS]['insert_time']


def test_increments_per_hour1():
    """
    Test increments per hour
    :query:
        SELECT
            increments(hour, 1, timestamp), MIN(timestamp), MAX(timestamp),
            MIN(value), MAX(value), MIN(value), AVG(value), COUNT(*)
        FROM
            table_name
        ORDER BY
            MIN(timestamp), MAX(timestamp)
    :assert:
        values are consistent in terms of row count + values
    """
    hour = 1
    query = (f"SELECT increments(hour, {hour}, timestamp), "
            +"min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_val, "
            +f"max(value) as max_val, avg(value) as avg_val, count(*) as row_count FROM {TABLE_NAME} "
            +"ORDER BY min_ts, max_ts")
    results = get_results(query=query, sql=True, networking=True)
    print(results)
    assert len(results) == len(EXPECT_RESULTS[NUM_ROWS]['increments_per_hour'][hour])
    assert results == EXPECT_RESULTS[NUM_ROWS]['increments_per_hour'][hour]


def test_increments_per_hour2():
    """
    Test increments per 2 hour
    :query:
        SELECT
            increments(hour, 2, timestamp), MIN(timestamp), MAX(timestamp),
            MIN(value), MAX(value), MIN(value), AVG(value), COUNT(*)
        FROM
            table_name
        ORDER BY
            MIN(timestamp), MAX(timestamp)
    :assert:
        values are consistent in terms of row count + values
    """
    hour = 2
    query = (f"SELECT increments(hour, {hour}, timestamp), "
            +"min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_val, "
            +f"max(value) as max_val, avg(value) as avg_val, count(*) as row_count FROM {TABLE_NAME} "
            +"ORDER BY min_ts, max_ts")
    results = get_results(query=query, sql=True, networking=True)
    assert len(results) == len(EXPECT_RESULTS[NUM_ROWS]['increments_per_hour'][hour])
    assert results == EXPECT_RESULTS[NUM_ROWS]['increments_per_hour'][hour]


def test_increments_per_hour6():
    """
    Test increments per 6 hour
    :query:
        SELECT
            increments(hour, 6, timestamp), MIN(timestamp), MAX(timestamp),
            MIN(value), MAX(value), MIN(value), AVG(value), COUNT(*)
        FROM
            table_name
        ORDER BY
            MIN(timestamp), MAX(timestamp)
    :assert:
        values are consistent in terms of row count + values
    """
    hour = 6
    query = (f"SELECT increments(hour, {hour}, timestamp), "
            +"min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_val, "
            +f"max(value) as max_val, avg(value) as avg_val, count(*) as row_count FROM {TABLE_NAME} "
            +"ORDER BY min_ts, max_ts")
    results = get_results(query=query, sql=True, networking=True)
    assert len(results) == len(EXPECT_RESULTS[NUM_ROWS]['increments_per_hour'][hour])
    assert results == EXPECT_RESULTS[NUM_ROWS]['increments_per_hour'][hour]


def test_increments_per_hour12():
    """
    Test increments per 12 hour
    :query:
        SELECT
            increments(hour, 12, timestamp), MIN(timestamp), MAX(timestamp),
            MIN(value), MAX(value), MIN(value), AVG(value), COUNT(*)
        FROM
            table_name
        ORDER BY
            MIN(timestamp), MAX(timestamp)
    :assert:
        values are consistent in terms of row count + values
    """
    hour = 12
    query = (f"SELECT increments(hour, {hour}, timestamp), "
            +"min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_val, "
            +f"max(value) as max_val, avg(value) as avg_val, count(*) as row_count FROM {TABLE_NAME} "
            +"ORDER BY min_ts, max_ts")
    results = get_results(query=query, sql=True, networking=True)
    assert len(results) == len(EXPECT_RESULTS[NUM_ROWS]['increments_per_hour'][hour])
    assert results == EXPECT_RESULTS[NUM_ROWS]['increments_per_hour'][hour]


def test_increments_per_hour24():
    """
    Test increments per 24 hour
    :query:
        SELECT
            increments(hour, 24, timestamp), MIN(timestamp), MAX(timestamp),
            MIN(value), MAX(value), MIN(value), AVG(value), COUNT(*)
        FROM
            table_name
        ORDER BY
            MIN(timestamp), MAX(timestamp)
    :assert:
        values are consistent in terms of row count + values
    """
    hour = 24
    query = (f"SELECT increments(hour, {hour}, timestamp), "
            +"min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_val, "
            +f"max(value) as max_val, avg(value) as avg_val, count(*) as row_count FROM {TABLE_NAME} "
            +"ORDER BY min_ts, max_ts")
    results = get_results(query=query, sql=True, networking=True)
    assert len(results) == len(EXPECT_RESULTS[NUM_ROWS]['increments_per_hour'][hour])
    assert results == EXPECT_RESULTS[NUM_ROWS]['increments_per_hour'][hour]


if __name__ == '__main__':
    test_increments_per_hour1()