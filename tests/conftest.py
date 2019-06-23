from hypothesis import (HealthCheck,
                        settings)

settings.register_profile('default',
                          deadline=None,
                          suppress_health_check=[HealthCheck.too_slow])
