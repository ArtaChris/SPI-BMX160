from adafruit_bus_device.spi_device import SPIDevice
from adafruit_bus_device.i2c_device import I2CDevice
from micropython import const
try:
    from struct import unpack
except ImportError:
    from ustruct import unpack
from time import sleep

# Chip ID
BMX160_CHIP_ID = const(0xD8)

# BMX160 Register map
BMX160_CHIP_ID_ADDR        = const(0x00)
BMX160_ERROR_REG_ADDR      = const(0x02)
BMX160_PMU_STATUS_ADDR     = const(0x03)

BMX160_MAG_DATA_ADDR       = const(0x04)
BMX160_RHALL_DATA_ADDR     = const(0x0A)
BMX160_GYRO_DATA_ADDR      = const(0x0C)
BMX160_ACCEL_DATA_ADDR     = const(0x12)
BMX160_SENSOR_TIME_ADDR    = const(0x18)

BMX160_STATUS_ADDR         = const(0x1B)

BMX160_INT_STATUS_ADDR     = const(0x1C)

BMX160_TEMP_DATA_ADDR      = const(0x20)

BMX160_ACCEL_CONFIG_ADDR   = const(0x40)
BMX160_ACCEL_RANGE_ADDR    = const(0x41)
BMX160_GYRO_CONFIG_ADDR    = const(0x42)
BMX160_GYRO_RANGE_ADDR     = const(0x43)
BMX160_MAG_CONFIG_ADDR        = const(0x44)

BMX160_MAG_IF_0_ADDR       = const(0x4C)
BMX160_MAG_IF_1_ADDR       = const(0x4D)
BMX160_MAG_IF_2_ADDR       = const(0x4E)
BMX160_MAG_IF_3_ADDR       = const(0x4F)
BMX160_INT_ENABLE_0_ADDR   = const(0x50)
BMX160_INT_ENABLE_1_ADDR   = const(0x51)
BMX160_INT_ENABLE_2_ADDR   = const(0x52)
BMX160_INT_OUT_CTRL_ADDR   = const(0x53)
BMX160_INT_LATCH_ADDR      = const(0x54)
BMX160_INT_MAP_0_ADDR      = const(0x55)
BMX160_INT_MAP_1_ADDR      = const(0x56)
BMX160_INT_MAP_2_ADDR      = const(0x57)
BMX160_INT_DATA_0_ADDR     = const(0x58)
BMX160_INT_DATA_1_ADDR     = const(0x59)
BMX160_INT_LOWHIGH_0_ADDR  = const(0x5A)
BMX160_INT_LOWHIGH_1_ADDR  = const(0x5B)
BMX160_INT_LOWHIGH_2_ADDR  = const(0x5C)
BMX160_INT_LOWHIGH_3_ADDR  = const(0x5D)
BMX160_INT_LOWHIGH_4_ADDR  = const(0x5E)
BMX160_INT_MOTION_0_ADDR   = const(0x5F)
BMX160_INT_MOTION_1_ADDR   = const(0x60)
BMX160_INT_MOTION_2_ADDR   = const(0x61)
BMX160_INT_MOTION_3_ADDR   = const(0x62)
BMX160_INT_TAP_0_ADDR      = const(0x63)
BMX160_INT_TAP_1_ADDR      = const(0x64)
BMX160_INT_ORIENT_0_ADDR   = const(0x65)
BMX160_INT_ORIENT_1_ADDR   = const(0x66)
BMX160_INT_FLAT_0_ADDR     = const(0x67)
BMX160_INT_FLAT_1_ADDR     = const(0x68)
BMX160_FOC_CONF_ADDR       = const(0x69)

BMX160_CONF_ADDR           = const(0x6A)
BMX160_SELF_TEST_ADDR      = const(0x6D)
BMX160_NV_CONF_ADDR        = const(0x70)

BMX160_ACCEL_BW_OSR4_AVG1   = const(0x00)
BMX160_ACCEL_BW_OSR2_AVG2   = const(0x01)
BMX160_ACCEL_BW_NORMAL_AVG4 = const(0x02)
BMX160_ACCEL_BW_AVG8        = const(0x03)
BMX160_ACCEL_BW_AVG16       = const(0x04)
BMX160_ACCEL_BW_AVG32       = const(0x05)
BMX160_ACCEL_BW_AVG64       = const(0x06)
BMX160_ACCEL_BW_AVG128      = const(0x07)

BMX160_GYRO_BW_OSR4         = const(0x00)
BMX160_GYRO_BW_OSR2         = const(0x01)
BMX160_GYRO_BW_NORMAL_MODE  = const(0x02)

# Self test configurations
BMX160_ACCEL_SELF_TEST_CONFIG        = const(0x2C)
BMX160_ACCEL_SELF_TEST_POSITIVE_EN   = const(0x0D)
BMX160_ACCEL_SELF_TEST_NEGATIVE_EN   = const(0x09)
BMX160_ACCEL_SELF_TEST_LIMIT         = const(8192)



# Command ##############################################
BMX160_COMMAND_REG_ADDR    = const(0x7E)

# Power mode settings
# Accel power mode
BMX160_ACCEL_NORMAL_MODE             = const(0x11)
BMX160_ACCEL_LOWPOWER_MODE           = const(0x12)
BMX160_ACCEL_SUSPEND_MODE            = const(0x10)

BMX160_ACCEL_MODES = [BMX160_ACCEL_NORMAL_MODE,
                      BMX160_ACCEL_LOWPOWER_MODE,
                      BMX160_ACCEL_SUSPEND_MODE]

# Gyro power mode
BMX160_GYRO_SUSPEND_MODE             = const(0x14)
BMX160_GYRO_NORMAL_MODE              = const(0x15)
BMX160_GYRO_FASTSTARTUP_MODE         = const(0x17)

BMX160_GYRO_MODES = [BMX160_GYRO_SUSPEND_MODE,
                     BMX160_GYRO_NORMAL_MODE,
                     BMX160_GYRO_FASTSTARTUP_MODE]

# Mag power mode
BMX160_MAG_SUSPEND_MODE              = const(0x18)
BMX160_MAG_NORMAL_MODE               = const(0x19)
BMX160_MAG_LOWPOWER_MODE             = const(0x1A)

BMX160_MAG_MODES = [BMX160_MAG_SUSPEND_MODE,
                    BMX160_MAG_NORMAL_MODE,
                    BMX160_MAG_LOWPOWER_MODE]

# Soft reset command
BMX160_SOFT_RESET_CMD      = const(0xB6)


# Accel Range
BMX160_ACCEL_RANGE_2G                = const(0x03)
BMX160_ACCEL_RANGE_4G                = const(0x05)
BMX160_ACCEL_RANGE_8G                = const(0x08)
BMX160_ACCEL_RANGE_16G               = const(0x0C)

BMX160_ACCEL_RANGE_CONSTANTS = [BMX160_ACCEL_RANGE_2G,
                                BMX160_ACCEL_RANGE_4G,
                                BMX160_ACCEL_RANGE_8G,
                                BMX160_ACCEL_RANGE_16G]
BMX160_ACCEL_RANGE_VALUES = [2, 4, 8, 16]


# Gyro Range
BMX160_GYRO_RANGE_2000_DPS           = const(0x00)
BMX160_GYRO_RANGE_1000_DPS           = const(0x01)
BMX160_GYRO_RANGE_500_DPS            = const(0x02)
BMX160_GYRO_RANGE_250_DPS            = const(0x03)
BMX160_GYRO_RANGE_125_DPS            = const(0x04)

BMX160_GYRO_RANGE_CONSTANTS = [BMX160_GYRO_RANGE_2000_DPS,
                               BMX160_GYRO_RANGE_1000_DPS,
                               BMX160_GYRO_RANGE_500_DPS,
                               BMX160_GYRO_RANGE_250_DPS,
                               BMX160_GYRO_RANGE_125_DPS]
BMX160_GYRO_RANGE_VALUES = [2000, 1000, 500, 250, 125]


# Output Data Rate settings
# Accel Output data rate
BMX160_ACCEL_ODR_0_78HZ              = const(0x01)
BMX160_ACCEL_ODR_1_56HZ              = const(0x02)
BMX160_ACCEL_ODR_3_12HZ              = const(0x03)
BMX160_ACCEL_ODR_6_25HZ              = const(0x04)
BMX160_ACCEL_ODR_12_5HZ              = const(0x05)
BMX160_ACCEL_ODR_25HZ                = const(0x06)
BMX160_ACCEL_ODR_50HZ                = const(0x07)
BMX160_ACCEL_ODR_100HZ               = const(0x08)
BMX160_ACCEL_ODR_200HZ               = const(0x09)
BMX160_ACCEL_ODR_400HZ               = const(0x0A)
BMX160_ACCEL_ODR_800HZ               = const(0x0B)
BMX160_ACCEL_ODR_1600HZ              = const(0x0C)

BMX160_ACCEL_ODR_CONSTANTS = [BMX160_ACCEL_ODR_0_78HZ,
                              BMX160_ACCEL_ODR_1_56HZ,
                              BMX160_ACCEL_ODR_3_12HZ,
                              BMX160_ACCEL_ODR_6_25HZ,
                              BMX160_ACCEL_ODR_12_5HZ,
                              BMX160_ACCEL_ODR_25HZ,
                              BMX160_ACCEL_ODR_50HZ,
                              BMX160_ACCEL_ODR_100HZ,
                              BMX160_ACCEL_ODR_200HZ,
                              BMX160_ACCEL_ODR_400HZ,
                              BMX160_ACCEL_ODR_800HZ,
                              BMX160_ACCEL_ODR_1600HZ]
BMX160_ACCEL_ODR_VALUES = [0.78, 1.56, 3.12, 6.25, 12.5, 25, 50, 100, 200, 400, 800, 1600]

# Gyro Output data rate
BMX160_GYRO_ODR_25HZ                 = const(0x06)
BMX160_GYRO_ODR_50HZ                 = const(0x07)
BMX160_GYRO_ODR_100HZ                = const(0x08)
BMX160_GYRO_ODR_200HZ                = const(0x09)
BMX160_GYRO_ODR_400HZ                = const(0x0A)
BMX160_GYRO_ODR_800HZ                = const(0x0B)
BMX160_GYRO_ODR_1600HZ               = const(0x0C)
BMX160_GYRO_ODR_3200HZ               = const(0x0D)

BMX160_GYRO_ODR_CONSTANTS = [BMX160_GYRO_ODR_25HZ,
                             BMX160_GYRO_ODR_50HZ,
                             BMX160_GYRO_ODR_100HZ,
                             BMX160_GYRO_ODR_200HZ,
                             BMX160_GYRO_ODR_400HZ,
                             BMX160_GYRO_ODR_800HZ,
                             BMX160_GYRO_ODR_1600HZ,
                             BMX160_GYRO_ODR_3200HZ]
BMX160_GYRO_ODR_VALUES = [25, 50, 100, 200, 400, 800, 1600, 3200]

# Mag sensor Output data rate
BMX160_MAG_ODR_0_78HZ                = const(0x01)
BMX160_MAG_ODR_1_56HZ                = const(0x02)
BMX160_MAG_ODR_3_12HZ                = const(0x03)
BMX160_MAG_ODR_6_25HZ                = const(0x04)
BMX160_MAG_ODR_12_5HZ                = const(0x05)
BMX160_MAG_ODR_25HZ                  = const(0x06)
BMX160_MAG_ODR_50HZ                  = const(0x07)
BMX160_MAG_ODR_100HZ                 = const(0x08)
BMX160_MAG_ODR_200HZ                 = const(0x09)
BMX160_MAG_ODR_400HZ                 = const(0x0A)
BMX160_MAG_ODR_800HZ                 = const(0x0B)

BMX160_MAG_ODR_CONSTANTS = [BMX160_MAG_ODR_0_78HZ,
                            BMX160_MAG_ODR_1_56HZ,
                            BMX160_MAG_ODR_3_12HZ,
                            BMX160_MAG_ODR_6_25HZ,
                            BMX160_MAG_ODR_12_5HZ,
                            BMX160_MAG_ODR_25HZ,
                            BMX160_MAG_ODR_50HZ,
                            BMX160_MAG_ODR_100HZ,
                            BMX160_MAG_ODR_200HZ,
                            BMX160_MAG_ODR_400HZ,
                            BMX160_MAG_ODR_800HZ]
BMX160_MAG_ODR_VALUES = [0.78, 1.56, 3.12, 6.25, 12.5, 25, 50, 100, 200, 400, 800]

# Accel, gyro and aux. sensor length and also their combined length definitions in FIFO
BMX160_FIFO_G_LENGTH                 = const(6)
BMX160_FIFO_A_LENGTH                 = const(6)
BMX160_FIFO_M_LENGTH                 = const(8)
BMX160_FIFO_GA_LENGTH                = const(12)
BMX160_FIFO_MA_LENGTH                = const(14)
BMX160_FIFO_MG_LENGTH                = const(14)
BMX160_FIFO_MGA_LENGTH               = const(20)

# I2C address
BMX160_I2C_ADDR            = const(0x68)
BMX160_I2C_ALT_ADDR        = const(0x69)  # alternate address
# Interface settings
BMX160_SPI_INTF            = const(1)
BMX160_I2C_INTF            = const(0)
BMX160_SPI_RD_MASK         = const(0x80)
BMX160_SPI_WR_MASK         = const(0x7F)

# Error related
BMX160_OK                  = const(0)
BMX160_ERROR               = const(-1)

# Each goes with a different sensitivity
BMX160_ACCEL_SENSE_2G                = const(16384)
BMX160_ACCEL_SENSE_4G                = const(8192)
BMX160_ACCEL_SENSE_8G                = const(4096)
BMX160_ACCEL_SENSE_16G               = const(2048)

BMX160_GYRO_SENSE_2000_DPS           = 16.4
BMX160_GYRO_SENSE_1000_DPS           = 32.8
BMX160_GYRO_SENSE_500_DPS            = 65.6
BMX160_GYRO_SENSE_250_DPS            = 131.2
BMX160_GYRO_SENSE_125_DPS            = 262.4

BMX160_MAG_SENSE                     = 0.0625

BMX160_MAX_SCLK = const(4000000)

class BMX160_SPI:
    txbuf = bytearray(8)
    rxbuf = bytearray(8)

    accel = [0, 0, 0]
    accel_range = BMX160_ACCEL_RANGE_4G
    accel_sens  = BMX160_ACCEL_SENSE_4G

    gyro  = [0, 0, 0]
    gyro_range  = BMX160_GYRO_RANGE_125_DPS
    gyro_sens   = BMX160_GYRO_SENSE_125_DPS

    mag   = [0, 0, 0]
    mag_sens    = BMX160_MAG_SENSE

    def __init__(self, spi, cs):
        self.spi_device = SPIDevice(spi, cs, baudrate=BMX160_MAX_SCLK, polarity=0, phase=0)

        self.txbuf[0] = BMX160_COMMAND_REG_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = BMX160_SOFT_RESET_CMD
        with self.spi_device as spi:
            spi.write(self.txbuf, end=2)

        self.txbuf[0] = 0x7F | BMX160_SPI_RD_MASK
        with self.spi_device as spi:
            spi.write(self.txbuf, end=1)
            spi.readinto(self.rxbuf, end=1)

        self.txbuf[0] = BMX160_CONF_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = 0x02
        with self.spi_device as spi:
            spi.write(self.txbuf, end=2)

        self.txbuf[0] = BMX160_NV_CONF_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = BMX160_SPI_INTF
        with self.spi_device as spi:
            spi.write(self.txbuf, end=2)

        self.init_accel()
        self.init_gyro()
        self.init_mag()

    def init_accel(self):
        # Set Power Mode
        self.txbuf[0] = BMX160_COMMAND_REG_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = BMX160_ACCEL_NORMAL_MODE
        with self.spi_device as spi:
            spi.write(self.txbuf, end=2)

        # Set ODR and FSR
        self.txbuf[0] = BMX160_ACCEL_CONFIG_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = (BMX160_ACCEL_ODR_800HZ | (BMX160_ACCEL_BW_OSR2_AVG2 << 4)) & 0x7F
        self.txbuf[2] = self.accel_range & 0x0F
        with self.spi_device as spi:
            spi.write(self.txbuf, end=3)
        print(bytes(self.txbuf))
        for i in self.txbuf:
            print("%6s" % (hex(i)), end='')
        print('\n')
        self.txbuf[0] = BMX160_ACCEL_CONFIG_ADDR | BMX160_SPI_RD_MASK
        with self.spi_device as spi:
            spi.write(self.txbuf, end=1)
            spi.readinto(self.rxbuf, end=2)
        for i in self.rxbuf:
            print("%6s" % (hex(i)), end='')
        print('\n')

    def init_gyro(self):
        # Set Power Mode
        self.txbuf[0] = BMX160_COMMAND_REG_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = BMX160_GYRO_NORMAL_MODE
        with self.spi_device as spi:
            spi.write(self.txbuf, end=2)

        # Set ODR and FSR
        self.txbuf[0] = BMX160_GYRO_CONFIG_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = (BMX160_GYRO_ODR_800HZ | (BMX160_GYRO_BW_OSR4 << 4)) & 0x3F
        self.txbuf[2] = self.gyro_range & 0x07
        with self.spi_device as spi:
            spi.write(self.txbuf, end=3)

    def init_mag(self):
        # Set Power Mode
        self.txbuf[0] = BMX160_COMMAND_REG_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = BMX160_MAG_NORMAL_MODE
        with self.spi_device as spi:
            spi.write(self.txbuf, end=2)

        # Set ODR
        self.txbuf[0] = BMX160_MAG_CONFIG_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = BMX160_MAG_ODR_200HZ & 0x0F
        with self.spi_device as spi:
            spi.write(self.txbuf, end=2)

    def read_accel(self):
        self.txbuf[0] = BMX160_ACCEL_DATA_ADDR | BMX160_SPI_RD_MASK
        with self.spi_device as spi:
            spi.write(self.txbuf, end=1)
            spi.readinto(self.rxbuf, end=6)

        self.accel[0:3] = unpack('<hhhh', bytes(self.rxbuf))[0:3]
        self.accel[0] = self.accel[0] / self.accel_sens * 9.81
        self.accel[1] = self.accel[1] / self.accel_sens * 9.81
        self.accel[2] = self.accel[2] / self.accel_sens * 9.81

        return self.accel

    def read_gyro(self):
        self.txbuf[0] = BMX160_GYRO_DATA_ADDR | BMX160_SPI_RD_MASK
        with self.spi_device as spi:
            spi.write(self.txbuf, end=1)
            spi.readinto(self.rxbuf, end=6)

        self.gyro[0], self.gyro[1], self.gyro[2] = unpack('<hhhh', bytes(self.rxbuf))[0:3]
        self.gyro[0] = self.gyro[0] / self.gyro_sens
        self.gyro[1] = self.gyro[1] / self.gyro_sens
        self.gyro[2] = self.gyro[2] / self.gyro_sens

        return self.gyro

    def read_mag(self):
        self.txbuf[0] = BMX160_MAG_DATA_ADDR | BMX160_SPI_RD_MASK
        with self.spi_device as spi:
            spi.write(self.txbuf, end=1)
            spi.readinto(self.rxbuf, end=6)

        self.mag, self.mag[1], self.mag[2] = unpack('<hhhh', bytes(self.rxbuf))[0:3]
        self.mag[0] = self.mag[0] / self.mag_sens
        self.mag[1] = self.mag[1] / self.mag_sens
        self.mag[2] = self.mag[2] / self.mag_sens

        return self.mag


BMX160_DELAY = 0.001


class BMX160_I2C:
    txbuf = bytearray(8)
    rxbuf = bytearray(8)
    
    accel = [0, 0, 0]
    accel_range = BMX160_ACCEL_RANGE_4G
    accel_sens = BMX160_ACCEL_SENSE_4G
    
    gyro = [0, 0, 0]
    gyro_range = BMX160_GYRO_RANGE_250_DPS
    gyro_sens = BMX160_GYRO_SENSE_250_DPS
    
    mag = [0, 0, 0]
    mag_sens = BMX160_MAG_SENSE
    
    def __init__(self, i2c, address=BMX160_I2C_ADDR):
        self.i2c_device = I2CDevice(i2c, address)
        
        sleep(BMX160_DELAY)
        
        self.txbuf[0] = BMX160_COMMAND_REG_ADDR
        self.txbuf[1] = BMX160_SOFT_RESET_CMD
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=2)
        
        sleep(BMX160_DELAY)
        
        self.txbuf[0] = 0x7F
        with self.i2c_device as i2c:
            i2c.write(self.txbuf, end=1)
            i2c.readinto(self.rxbuf, end=1)
        
        sleep(BMX160_DELAY)
        
        self.txbuf[0] = BMX160_CONF_ADDR
        self.txbuf[1] = 0x02
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=2)
        
        sleep(BMX160_DELAY)
        
        self.txbuf[0] = BMX160_NV_CONF_ADDR
        self.txbuf[1] = 0x00  # BMX160_SPI_INTF
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=2)
        
        sleep(BMX160_DELAY)
        
        self.init_accel()
        self.init_gyro()
        # self.init_mag()
    
    def init_accel(self):
        # Set Power Mode
        self.txbuf[0] = BMX160_COMMAND_REG_ADDR
        self.txbuf[1] = BMX160_ACCEL_NORMAL_MODE
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=2)
        sleep(BMX160_DELAY)
        # Set ODR and FSR
        self.txbuf[0] = BMX160_ACCEL_CONFIG_ADDR
        self.txbuf[1] = (BMX160_ACCEL_ODR_800HZ | (BMX160_ACCEL_BW_OSR2_AVG2 << 4)) & 0x7F
        self.txbuf[2] = self.accel_range & 0x0F
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=3)
        sleep(BMX160_DELAY)
        
        print(bytes(self.txbuf))
        for i in self.txbuf:
            print("%6s" % (hex(i)), end='')
        print('\n')
        self.txbuf[0] = BMX160_ACCEL_CONFIG_ADDR
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=1)
            spi.readinto(self.rxbuf, end=2)
        
        for i in self.rxbuf:
            print("%6s" % (hex(i)), end='')
        print('\n')
    
    def init_gyro(self):
        # Set Power Mode
        self.txbuf[0] = BMX160_COMMAND_REG_ADDR
        self.txbuf[1] = BMX160_GYRO_NORMAL_MODE
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=2)
        sleep(BMX160_DELAY)
        # Set ODR and FSR
        self.txbuf[0] = BMX160_GYRO_CONFIG_ADDR
        self.txbuf[1] = (BMX160_GYRO_ODR_800HZ | (BMX160_GYRO_BW_OSR4 << 4)) & 0x3F
        self.txbuf[2] = self.gyro_range & 0x07
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=3)
        sleep(BMX160_DELAY)
    
    def init_mag(self):
        # Set Power Mode
        self.txbuf[0] = BMX160_COMMAND_REG_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = BMX160_MAG_NORMAL_MODE
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=2)
        
        # Set ODR
        self.txbuf[0] = BMX160_MAG_CONFIG_ADDR & BMX160_SPI_WR_MASK
        self.txbuf[1] = BMX160_MAG_ODR_200HZ & 0x0F
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=2)
    
    def read_accel(self):
        self.txbuf[0] = BMX160_ACCEL_DATA_ADDR | BMX160_SPI_RD_MASK
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=1)
            sleep(BMX160_DELAY)
            spi.readinto(self.rxbuf, end=6)
        
        self.accel[0:3] = unpack('<hhhh', bytes(self.rxbuf))[0:3]
        self.accel[0] = self.accel[0] / self.accel_sens * 9.81
        self.accel[1] = self.accel[1] / self.accel_sens * 9.81
        self.accel[2] = self.accel[2] / self.accel_sens * 9.81
        
        return self.accel
    
    def read_gyro(self):
        self.txbuf[0] = BMX160_GYRO_DATA_ADDR | BMX160_SPI_RD_MASK
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=1)
            sleep(BMX160_DELAY)
            spi.readinto(self.rxbuf, end=6)
        
        self.gyro[0:3] = unpack('<hhhh', bytes(self.rxbuf))[0:3]
        self.gyro[0] = self.gyro[0] / self.gyro_sens * 0.0174533
        self.gyro[1] = self.gyro[1] / self.gyro_sens * 0.0174533
        self.gyro[2] = self.gyro[2] / self.gyro_sens * 0.0174533
        
        return self.gyro
    
    def read_mag(self):
        self.txbuf[0] = BMX160_MAG_DATA_ADDR | BMX160_SPI_RD_MASK
        with self.i2c_device as spi:
            spi.write(self.txbuf, end=1)
            spi.readinto(self.rxbuf, end=6)
        
        self.mag, self.mag[1], self.mag[2] = unpack('<hhhh', bytes(self.rxbuf))[0:3]
        self.mag[0] = self.mag[0] / self.mag_sens
        self.mag[1] = self.mag[1] / self.mag_sens
        self.mag[2] = self.mag[2] / self.mag_sens
        
        return self.mag

