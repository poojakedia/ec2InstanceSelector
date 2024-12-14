import pynecone as pc

class CloudservicescostanalysisConfig(pc.Config):
    pass

config = CloudservicescostanalysisConfig(
    app_name="cloudServicesCostAnalysis",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)