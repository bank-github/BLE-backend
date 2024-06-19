
import math as math

# สร้างคลาส Kalman Filter
class KalmanFilter:
    def __init__(self, process_variance, measurement_variance):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def update(self, measurement):
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance

        blending_factor = priori_error_estimate / (priori_error_estimate + self.measurement_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

        return self.posteri_estimate
    
# สร้าง Kalman filter ด้วยค่าความแปรปรวนของกระบวนการและการวัด
kf = KalmanFilter(process_variance=1e-5, measurement_variance=4)


# ข้อมูลตัวอย่างของค่า RSSI
print('================================')
for dt in data:
    rssi_values = []
    for rssi in dt['rssi']:
        rssi_values.append(rssi['rssi'])
        #ลื่นค่า RSSI โดยใช้ Kalman filter
        smoothed_rssi_values = [kf.update(signal) for signal in rssi_values]

        print("ค่า RSSI ต้นฉบับ:", rssi_values)
        smoothed_rssi_values = sum(smoothed_rssi_values)/len(smoothed_rssi_values)
        print("ค่า RSSI ที่ Mac:",dt['mac'], " : ", round(smoothed_rssi_values,2))
print('================================')

