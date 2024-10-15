from athlon_flex_api.api import AthlonFlexApi
from athlon_flex_api.models.filters.vehicle_cluster_filter import AllVehicleClusters

api = AthlonFlexApi(
    email="aucke.bos97@gmail.com",
    password="K*iGrKGIZ$30OvO3l",
    gross_yearly_income=60000,
)
clusters = api.vehicle_clusters(filter_=AllVehicleClusters())
print(clusters)
