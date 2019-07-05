class Config(object):
  """
  Common configs
  """

  # Configs common across all environments

class DevelopmentConfig(object):
  """
  Development configurations
  """
  DEBUG = True
  SQLALCHEMY_ECHO = True

class ProductionConfig(object):
  """
  Production configurations
  """
  DEBUG = False

app_config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig
}