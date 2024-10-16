from netbox.api.routers import NetBoxRouter
from . import views

router = NetBoxRouter()
router.APIRootView = views.SlurpitRootView
router.register("planning", views.SlurpitPlanningViewSet)
router.register("planning-data", views.SlurpitSnapshotViewSet)
router.register("device", views.DeviceViewSet)
router.register("test", views.SlurpitTestAPIView, basename="test")
router.register("netbox-device", views.SlurpitDeviceView)
router.register("ipam", views.SlurpitIPAMView)
router.register("interface", views.SlurpitInterfaceView)
router.register("prefix", views.SlurpitPrefixView)
router.register("vlan", views.SlurpitVLANView)
app_name = 'slurpit_netbox-api'
urlpatterns = router.urls
