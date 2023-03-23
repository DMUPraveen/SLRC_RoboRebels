class PID:
    def __init__(self, Kp: float, Kd: float, Ki: float):
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.set_point = 0.0
        self.error = 0.0
        self.previous_measurement = 0.0
        self.accumulated_error = 0.0
        self.previous_error = 0.0

    def create_copy(self):
        pid = PID(self.Kp, self.Kd, self.Ki)
        pid.set_set_point(self.set_point)
        return pid

    def set_set_point(self, value: float):
        self.set_point = value

    def control(self, measurement: float):
        error = self.set_point - measurement

        control_signal = self.Kp*error

        self.previous_error = error
        self.previous_measurement = measurement

        return control_signal

    def __call__(self, measurement: float):
        return self.control(measurement)
