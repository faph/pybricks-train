from pybricks.hubs import CityHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Color, Port
from pybricks.tools import wait

import pylc


def run():
    hub = CityHub()
    remote = Remote()
    remote.light.on(Color.WHITE * 0.1)

    logical_machine = LogicalMachine()
    outputs = outputs_map(hub)
    scan_timer = pylc.ScanTimer(200)

    while True:
        with scan_timer:
            logical_machine.execute(buttons_pressed=remote.buttons.pressed())
            for output_name, output_fn in outputs.items():
                output_fn(getattr(logical_machine, output_name))

def outputs_map(hub):
    return {
        "motor_speed": Motor(port=Port.A).run,
        "light_color": hub.light.on,
    }

class LogicalMachine:
    """Main logical component"""

    def __init__(self):
        """Initial state"""
        # Variable state
        self.motor_speed = 0  # The current motor speed, deg/s
        self.is_breaking = False  # Whether we are coming to a stop
        self.light_color = Color.ORANGE * 0.5
        
        # Fixed values
        self.max_speed = 1000  # deg/s
        self.accelaration_rate = 40  # deg/s/s
        self.deceleration_rate = 40  # deg/s/s
        self.braking_rate = self.deceleration_rate * 3  # deg/s/s

    def execute(self, buttons_pressed):
        """Execute the logic as part of a single scan"""
        if Button.LEFT_PLUS in buttons_pressed:
            self.motor_speed += self.accelaration_rate * pylc.current_scan_time / 1000
            self.motor_speed = min(
                self.motor_speed,
                self.max_speed
            )
            self.is_breaking = False
        elif Button.LEFT_MINUS in buttons_pressed:
            self.motor_speed -= self.deceleration_rate * pylc.current_scan_time / 1000
            self.motor_speed = max(
                - self.max_speed,
                self.motor_speed
            )
            self.is_breaking = False
        elif Button.LEFT in buttons_pressed:
            self.is_breaking = True
        elif Button.RIGHT in buttons_pressed:
            self.motor_speed = 0

        if self.is_breaking:
            braking_speed_diff = self.braking_rate * pylc.current_scan_time / 1000
            if abs(self.motor_speed) <= braking_speed_diff:
                self.motor_speed = 0
            else:
                self.motor_speed -= self._direction() * braking_speed_diff

        if self.motor_speed > 0:
            self.light_color = Color.WHITE * 0.5
        elif self.motor_speed < 0:
            self.light_color = Color.RED * 0.5

        print(self.motor_speed)

    def _direction(self):
        """Return the direction of the motor"""
        if self.motor_speed >= 0:
            return 1
        else:
            return -1


if __name__ == "__main__":
    run()