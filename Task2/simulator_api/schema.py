import graphene
from graphene_django import DjangoObjectType
from .models import SimulatorDetail,DatasetConfiguration,SeasonalityComponent

class SimulatorType(DjangoObjectType):
    class Meta:
        model= SimulatorDetail
        field=("status","start_date","end_date","scheduler","name","sink_name","time_series_type","producer_type","process_id")
class DatasetConfigurationType(DjangoObjectType):
    class Meta :
        model = DatasetConfiguration
        field=("generator_id","attribute_id","frequency","noise_level","trend_coefficients","missing_percentage","outlier_percentage","cycle_component_frequency","status","time_series")
     
class SeasonalityComponentType(DjangoObjectType):
    class Meta:
        model = SeasonalityComponent
        field = ("amplitude","phase_shift","frequency_type","frequency_multiplier","dataset_configuration")

class UpdateSchedulerMutation(graphene.Mutation):
    class Arguments:
        simulator_id = graphene.ID(required=True)
        scheduler = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, simulator_id, scheduler):
        simulator = SimulatorDetail.objects.get(id=simulator_id)
        simulator.scheduler = scheduler
        simulator.save()
        return UpdateSchedulerMutation(success=True)

class UpdateSinkNameMutation(graphene.Mutation):
    class Arguments:
        simulator_id = graphene.ID(required=True)
        sink_name = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, simulator_id, sink_name):
        simulator = SimulatorDetail.objects.get(id=simulator_id)
        simulator.sink_name = sink_name
        simulator.save()
        return UpdateSinkNameMutation(success=True)
    
class Mutation(graphene.ObjectType):
    update_scheduler = UpdateSchedulerMutation.Field()
    update_sink_name = UpdateSinkNameMutation.Field()
    
class Query(graphene.ObjectType):
    all_simulators=graphene.List(SimulatorType)
    all_dataset_configurations=graphene.List(DatasetConfigurationType)
    all_seasonality_components=graphene.List(SeasonalityComponentType)
    def resolve_all_simulators(root,info):
        return SimulatorDetail.objects.all()
    def resolve_all_dataset_configurations(root,info):
        return DatasetConfiguration.objects.all()    
    def resolve_all_seasonality_components(root,info):
        return SeasonalityComponent.objects.all()    


schema=graphene.Schema(query=Query,mutation=Mutation)    