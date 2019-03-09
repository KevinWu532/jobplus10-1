class BaseConfig(object):
    '''配置基类'''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'jobplus10-1'
    INDEX_PER_PAGE = 9
    ADMIN_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
    '''开发环境'''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/jobplus?charset=utf8'

class ProductionConfig(BaseConfig):
    '''生产环境'''
    pass

class TestingConfig(BaseConfig):
    pass

configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
        }

