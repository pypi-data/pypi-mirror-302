"""Solver settings."""

from ansys.fluent.core.solver.settings_builtin_bases import _SingletonSetting, _CreatableNamedObjectSetting, _NonCreatableNamedObjectSetting


__all__ = [
    "Setup",
    "General",
    "Models",
    "Multiphase",
    "Energy",
    "Viscous",
    "Radiation",
    "Species",
    "DiscretePhase",
    "Injections",
    "Injection",
    "VirtualBladeModel",
    "Optics",
    "Structure",
    "Ablation",
    "EChemistry",
    "Battery",
    "SystemCoupling",
    "Sofc",
    "Pemfc",
    "Materials",
    "FluidMaterials",
    "FluidMaterial",
    "SolidMaterials",
    "SolidMaterial",
    "MixtureMaterials",
    "MixtureMaterial",
    "ParticleMixtureMaterials",
    "ParticleMixtureMaterial",
    "CellZoneConditions",
    "CellZoneCondition",
    "FluidCellZones",
    "FluidCellZone",
    "SolidCellZones",
    "SolidCellZone",
    "BoundaryConditions",
    "BoundaryCondition",
    "AxisBoundaries",
    "AxisBoundary",
    "DegassingBoundaries",
    "DegassingBoundary",
    "ExhaustFanBoundaries",
    "ExhaustFanBoundary",
    "FanBoundaries",
    "FanBoundary",
    "GeometryBoundaries",
    "GeometryBoundary",
    "InletVentBoundaries",
    "InletVentBoundary",
    "IntakeFanBoundaries",
    "IntakeFanBoundary",
    "InterfaceBoundaries",
    "InterfaceBoundary",
    "InteriorBoundaries",
    "InteriorBoundary",
    "MassFlowInlets",
    "MassFlowInlet",
    "MassFlowOutlets",
    "MassFlowOutlet",
    "NetworkBoundaries",
    "NetworkBoundary",
    "NetworkEndBoundaries",
    "NetworkEndBoundary",
    "OutflowBoundaries",
    "OutflowBoundary",
    "OutletVentBoundaries",
    "OutletVentBoundary",
    "OversetBoundaries",
    "OversetBoundary",
    "PeriodicBoundaries",
    "PeriodicBoundary",
    "PorousJumpBoundaries",
    "PorousJumpBoundary",
    "PressureFarFieldBoundaries",
    "PressureFarFieldBoundary",
    "PressureInlets",
    "PressureInlet",
    "PressureOutlets",
    "PressureOutlet",
    "RadiatorBoundaries",
    "RadiatorBoundary",
    "RansLesInterfaceBoundaries",
    "RansLesInterfaceBoundary",
    "RecirculationInlets",
    "RecirculationInlet",
    "RecirculationOutlets",
    "RecirculationOutlet",
    "ShadowBoundaries",
    "ShadowBoundary",
    "SymmetryBoundaries",
    "SymmetryBoundary",
    "VelocityInlets",
    "VelocityInlet",
    "WallBoundaries",
    "WallBoundary",
    "NonReflectingBoundaries",
    "NonReflectingBoundary",
    "PerforatedWallBoundaries",
    "PerforatedWallBoundary",
    "MeshInterfaces",
    "DynamicMesh",
    "ReferenceValues",
    "ReferenceFrames",
    "ReferenceFrame",
    "NamedExpressions",
    "NamedExpression",
    "Solution",
    "Methods",
    "Controls",
    "ReportDefinitions",
    "Monitor",
    "Residual",
    "ReportFiles",
    "ReportFile",
    "ReportPlots",
    "ReportPlot",
    "ConvergenceConditions",
    "CellRegisters",
    "CellRegister",
    "Initialization",
    "CalculationActivity",
    "ExecuteCommands",
    "CaseModification",
    "RunCalculation",
    "Results",
    "Surfaces",
    "PointSurfaces",
    "PointSurface",
    "LineSurfaces",
    "LineSurface",
    "RakeSurfaces",
    "RakeSurface",
    "PlaneSurfaces",
    "PlaneSurface",
    "IsoSurfaces",
    "IsoSurface",
    "IsoClips",
    "IsoClip",
    "ZoneSurfaces",
    "ZoneSurface",
    "PartitionSurfaces",
    "PartitionSurface",
    "TransformSurfaces",
    "TransformSurface",
    "ImprintSurfaces",
    "ImprintSurface",
    "PlaneSlices",
    "PlaneSlice",
    "SphereSlices",
    "SphereSlice",
    "QuadricSurfaces",
    "QuadricSurface",
    "SurfaceCells",
    "SurfaceCell",
    "ExpressionVolumes",
    "ExpressionVolume",
    "GroupSurfaces",
    "GroupSurface",
    "Graphics",
    "Meshes",
    "Mesh",
    "Contours",
    "Contour",
    "Vectors",
    "Vector",
    "Pathlines",
    "Pathline",
    "ParticleTracks",
    "ParticleTrack",
    "LICs",
    "LIC",
    "Plots",
    "XYPlots",
    "XYPlot",
    "Histogram",
    "CumulativePlots",
    "CumulativePlot",
    "ProfileData",
    "InterpolatedData",
    "Scenes",
    "Scene",
    "SceneAnimation",
    "Report",
    "DiscretePhaseHistogram",
    "Fluxes",
    "SurfaceIntegrals",
    "VolumeIntegrals",
    "InputParameters",
    "OutputParameters",
    "CustomFieldFunctions",
    "CustomFieldFunction",
    "CustomVectors",
    "CustomVector",
    "SimulationReports",
]

class Setup(_SingletonSetting):
    """Setup setting."""

class General(_SingletonSetting):
    """General setting."""

class Models(_SingletonSetting):
    """Models setting."""

class Multiphase(_SingletonSetting):
    """Multiphase setting."""

class Energy(_SingletonSetting):
    """Energy setting."""

class Viscous(_SingletonSetting):
    """Viscous setting."""

class Radiation(_SingletonSetting):
    """Radiation setting."""

class Species(_SingletonSetting):
    """Species setting."""

class DiscretePhase(_SingletonSetting):
    """DiscretePhase setting."""

class Injections(_SingletonSetting):
    """Injections setting."""

class Injection(_CreatableNamedObjectSetting):
    """Injection setting."""

class VirtualBladeModel(_SingletonSetting):
    """VirtualBladeModel setting."""

class Optics(_SingletonSetting):
    """Optics setting."""

class Structure(_SingletonSetting):
    """Structure setting."""

class Ablation(_SingletonSetting):
    """Ablation setting."""

class EChemistry(_SingletonSetting):
    """EChemistry setting."""

class Battery(_SingletonSetting):
    """Battery setting."""

class SystemCoupling(_SingletonSetting):
    """SystemCoupling setting."""

class Sofc(_SingletonSetting):
    """Sofc setting."""

class Pemfc(_SingletonSetting):
    """Pemfc setting."""

class Materials(_SingletonSetting):
    """Materials setting."""

class FluidMaterials(_SingletonSetting):
    """FluidMaterials setting."""

class FluidMaterial(_CreatableNamedObjectSetting):
    """FluidMaterial setting."""

class SolidMaterials(_SingletonSetting):
    """SolidMaterials setting."""

class SolidMaterial(_CreatableNamedObjectSetting):
    """SolidMaterial setting."""

class MixtureMaterials(_SingletonSetting):
    """MixtureMaterials setting."""

class MixtureMaterial(_CreatableNamedObjectSetting):
    """MixtureMaterial setting."""

class ParticleMixtureMaterials(_SingletonSetting):
    """ParticleMixtureMaterials setting."""

class ParticleMixtureMaterial(_CreatableNamedObjectSetting):
    """ParticleMixtureMaterial setting."""

class CellZoneConditions(_SingletonSetting):
    """CellZoneConditions setting."""

class CellZoneCondition(_NonCreatableNamedObjectSetting):
    """CellZoneCondition setting."""

class FluidCellZones(_SingletonSetting):
    """FluidCellZones setting."""

class FluidCellZone(_CreatableNamedObjectSetting):
    """FluidCellZone setting."""

class SolidCellZones(_SingletonSetting):
    """SolidCellZones setting."""

class SolidCellZone(_CreatableNamedObjectSetting):
    """SolidCellZone setting."""

class BoundaryConditions(_SingletonSetting):
    """BoundaryConditions setting."""

class BoundaryCondition(_NonCreatableNamedObjectSetting):
    """BoundaryCondition setting."""

class AxisBoundaries(_SingletonSetting):
    """AxisBoundaries setting."""

class AxisBoundary(_CreatableNamedObjectSetting):
    """AxisBoundary setting."""

class DegassingBoundaries(_SingletonSetting):
    """DegassingBoundaries setting."""

class DegassingBoundary(_CreatableNamedObjectSetting):
    """DegassingBoundary setting."""

class ExhaustFanBoundaries(_SingletonSetting):
    """ExhaustFanBoundaries setting."""

class ExhaustFanBoundary(_CreatableNamedObjectSetting):
    """ExhaustFanBoundary setting."""

class FanBoundaries(_SingletonSetting):
    """FanBoundaries setting."""

class FanBoundary(_CreatableNamedObjectSetting):
    """FanBoundary setting."""

class GeometryBoundaries(_SingletonSetting):
    """GeometryBoundaries setting."""

class GeometryBoundary(_CreatableNamedObjectSetting):
    """GeometryBoundary setting."""

class InletVentBoundaries(_SingletonSetting):
    """InletVentBoundaries setting."""

class InletVentBoundary(_CreatableNamedObjectSetting):
    """InletVentBoundary setting."""

class IntakeFanBoundaries(_SingletonSetting):
    """IntakeFanBoundaries setting."""

class IntakeFanBoundary(_CreatableNamedObjectSetting):
    """IntakeFanBoundary setting."""

class InterfaceBoundaries(_SingletonSetting):
    """InterfaceBoundaries setting."""

class InterfaceBoundary(_CreatableNamedObjectSetting):
    """InterfaceBoundary setting."""

class InteriorBoundaries(_SingletonSetting):
    """InteriorBoundaries setting."""

class InteriorBoundary(_CreatableNamedObjectSetting):
    """InteriorBoundary setting."""

class MassFlowInlets(_SingletonSetting):
    """MassFlowInlets setting."""

class MassFlowInlet(_CreatableNamedObjectSetting):
    """MassFlowInlet setting."""

class MassFlowOutlets(_SingletonSetting):
    """MassFlowOutlets setting."""

class MassFlowOutlet(_CreatableNamedObjectSetting):
    """MassFlowOutlet setting."""

class NetworkBoundaries(_SingletonSetting):
    """NetworkBoundaries setting."""

class NetworkBoundary(_CreatableNamedObjectSetting):
    """NetworkBoundary setting."""

class NetworkEndBoundaries(_SingletonSetting):
    """NetworkEndBoundaries setting."""

class NetworkEndBoundary(_CreatableNamedObjectSetting):
    """NetworkEndBoundary setting."""

class OutflowBoundaries(_SingletonSetting):
    """OutflowBoundaries setting."""

class OutflowBoundary(_CreatableNamedObjectSetting):
    """OutflowBoundary setting."""

class OutletVentBoundaries(_SingletonSetting):
    """OutletVentBoundaries setting."""

class OutletVentBoundary(_CreatableNamedObjectSetting):
    """OutletVentBoundary setting."""

class OversetBoundaries(_SingletonSetting):
    """OversetBoundaries setting."""

class OversetBoundary(_CreatableNamedObjectSetting):
    """OversetBoundary setting."""

class PeriodicBoundaries(_SingletonSetting):
    """PeriodicBoundaries setting."""

class PeriodicBoundary(_CreatableNamedObjectSetting):
    """PeriodicBoundary setting."""

class PorousJumpBoundaries(_SingletonSetting):
    """PorousJumpBoundaries setting."""

class PorousJumpBoundary(_CreatableNamedObjectSetting):
    """PorousJumpBoundary setting."""

class PressureFarFieldBoundaries(_SingletonSetting):
    """PressureFarFieldBoundaries setting."""

class PressureFarFieldBoundary(_CreatableNamedObjectSetting):
    """PressureFarFieldBoundary setting."""

class PressureInlets(_SingletonSetting):
    """PressureInlets setting."""

class PressureInlet(_CreatableNamedObjectSetting):
    """PressureInlet setting."""

class PressureOutlets(_SingletonSetting):
    """PressureOutlets setting."""

class PressureOutlet(_CreatableNamedObjectSetting):
    """PressureOutlet setting."""

class RadiatorBoundaries(_SingletonSetting):
    """RadiatorBoundaries setting."""

class RadiatorBoundary(_CreatableNamedObjectSetting):
    """RadiatorBoundary setting."""

class RansLesInterfaceBoundaries(_SingletonSetting):
    """RansLesInterfaceBoundaries setting."""

class RansLesInterfaceBoundary(_CreatableNamedObjectSetting):
    """RansLesInterfaceBoundary setting."""

class RecirculationInlets(_SingletonSetting):
    """RecirculationInlets setting."""

class RecirculationInlet(_CreatableNamedObjectSetting):
    """RecirculationInlet setting."""

class RecirculationOutlets(_SingletonSetting):
    """RecirculationOutlets setting."""

class RecirculationOutlet(_CreatableNamedObjectSetting):
    """RecirculationOutlet setting."""

class ShadowBoundaries(_SingletonSetting):
    """ShadowBoundaries setting."""

class ShadowBoundary(_CreatableNamedObjectSetting):
    """ShadowBoundary setting."""

class SymmetryBoundaries(_SingletonSetting):
    """SymmetryBoundaries setting."""

class SymmetryBoundary(_CreatableNamedObjectSetting):
    """SymmetryBoundary setting."""

class VelocityInlets(_SingletonSetting):
    """VelocityInlets setting."""

class VelocityInlet(_CreatableNamedObjectSetting):
    """VelocityInlet setting."""

class WallBoundaries(_SingletonSetting):
    """WallBoundaries setting."""

class WallBoundary(_CreatableNamedObjectSetting):
    """WallBoundary setting."""

class NonReflectingBoundaries(_SingletonSetting):
    """NonReflectingBoundaries setting."""

class NonReflectingBoundary(_NonCreatableNamedObjectSetting):
    """NonReflectingBoundary setting."""

class PerforatedWallBoundaries(_SingletonSetting):
    """PerforatedWallBoundaries setting."""

class PerforatedWallBoundary(_NonCreatableNamedObjectSetting):
    """PerforatedWallBoundary setting."""

class MeshInterfaces(_SingletonSetting):
    """MeshInterfaces setting."""

class DynamicMesh(_SingletonSetting):
    """DynamicMesh setting."""

class ReferenceValues(_SingletonSetting):
    """ReferenceValues setting."""

class ReferenceFrames(_SingletonSetting):
    """ReferenceFrames setting."""

class ReferenceFrame(_CreatableNamedObjectSetting):
    """ReferenceFrame setting."""

class NamedExpressions(_SingletonSetting):
    """NamedExpressions setting."""

class NamedExpression(_CreatableNamedObjectSetting):
    """NamedExpression setting."""

class Solution(_SingletonSetting):
    """Solution setting."""

class Methods(_SingletonSetting):
    """Methods setting."""

class Controls(_SingletonSetting):
    """Controls setting."""

class ReportDefinitions(_SingletonSetting):
    """ReportDefinitions setting."""

class Monitor(_SingletonSetting):
    """Monitor setting."""

class Residual(_SingletonSetting):
    """Residual setting."""

class ReportFiles(_SingletonSetting):
    """ReportFiles setting."""

class ReportFile(_CreatableNamedObjectSetting):
    """ReportFile setting."""

class ReportPlots(_SingletonSetting):
    """ReportPlots setting."""

class ReportPlot(_CreatableNamedObjectSetting):
    """ReportPlot setting."""

class ConvergenceConditions(_SingletonSetting):
    """ConvergenceConditions setting."""

class CellRegisters(_SingletonSetting):
    """CellRegisters setting."""

class CellRegister(_CreatableNamedObjectSetting):
    """CellRegister setting."""

class Initialization(_SingletonSetting):
    """Initialization setting."""

class CalculationActivity(_SingletonSetting):
    """CalculationActivity setting."""

class ExecuteCommands(_SingletonSetting):
    """ExecuteCommands setting."""

class CaseModification(_SingletonSetting):
    """CaseModification setting."""

class RunCalculation(_SingletonSetting):
    """RunCalculation setting."""

class Results(_SingletonSetting):
    """Results setting."""

class Surfaces(_SingletonSetting):
    """Surfaces setting."""

class PointSurfaces(_SingletonSetting):
    """PointSurfaces setting."""

class PointSurface(_CreatableNamedObjectSetting):
    """PointSurface setting."""

class LineSurfaces(_SingletonSetting):
    """LineSurfaces setting."""

class LineSurface(_CreatableNamedObjectSetting):
    """LineSurface setting."""

class RakeSurfaces(_SingletonSetting):
    """RakeSurfaces setting."""

class RakeSurface(_CreatableNamedObjectSetting):
    """RakeSurface setting."""

class PlaneSurfaces(_SingletonSetting):
    """PlaneSurfaces setting."""

class PlaneSurface(_CreatableNamedObjectSetting):
    """PlaneSurface setting."""

class IsoSurfaces(_SingletonSetting):
    """IsoSurfaces setting."""

class IsoSurface(_CreatableNamedObjectSetting):
    """IsoSurface setting."""

class IsoClips(_SingletonSetting):
    """IsoClips setting."""

class IsoClip(_CreatableNamedObjectSetting):
    """IsoClip setting."""

class ZoneSurfaces(_SingletonSetting):
    """ZoneSurfaces setting."""

class ZoneSurface(_CreatableNamedObjectSetting):
    """ZoneSurface setting."""

class PartitionSurfaces(_SingletonSetting):
    """PartitionSurfaces setting."""

class PartitionSurface(_CreatableNamedObjectSetting):
    """PartitionSurface setting."""

class TransformSurfaces(_SingletonSetting):
    """TransformSurfaces setting."""

class TransformSurface(_CreatableNamedObjectSetting):
    """TransformSurface setting."""

class ImprintSurfaces(_SingletonSetting):
    """ImprintSurfaces setting."""

class ImprintSurface(_CreatableNamedObjectSetting):
    """ImprintSurface setting."""

class PlaneSlices(_SingletonSetting):
    """PlaneSlices setting."""

class PlaneSlice(_CreatableNamedObjectSetting):
    """PlaneSlice setting."""

class SphereSlices(_SingletonSetting):
    """SphereSlices setting."""

class SphereSlice(_CreatableNamedObjectSetting):
    """SphereSlice setting."""

class QuadricSurfaces(_SingletonSetting):
    """QuadricSurfaces setting."""

class QuadricSurface(_CreatableNamedObjectSetting):
    """QuadricSurface setting."""

class SurfaceCells(_SingletonSetting):
    """SurfaceCells setting."""

class SurfaceCell(_CreatableNamedObjectSetting):
    """SurfaceCell setting."""

class ExpressionVolumes(_SingletonSetting):
    """ExpressionVolumes setting."""

class ExpressionVolume(_CreatableNamedObjectSetting):
    """ExpressionVolume setting."""

class GroupSurfaces(_SingletonSetting):
    """GroupSurfaces setting."""

class GroupSurface(_CreatableNamedObjectSetting):
    """GroupSurface setting."""

class Graphics(_SingletonSetting):
    """Graphics setting."""

class Meshes(_SingletonSetting):
    """Meshes setting."""

class Mesh(_CreatableNamedObjectSetting):
    """Mesh setting."""

class Contours(_SingletonSetting):
    """Contours setting."""

class Contour(_CreatableNamedObjectSetting):
    """Contour setting."""

class Vectors(_SingletonSetting):
    """Vectors setting."""

class Vector(_CreatableNamedObjectSetting):
    """Vector setting."""

class Pathlines(_SingletonSetting):
    """Pathlines setting."""

class Pathline(_CreatableNamedObjectSetting):
    """Pathline setting."""

class ParticleTracks(_SingletonSetting):
    """ParticleTracks setting."""

class ParticleTrack(_CreatableNamedObjectSetting):
    """ParticleTrack setting."""

class LICs(_SingletonSetting):
    """LICs setting."""

class LIC(_CreatableNamedObjectSetting):
    """LIC setting."""

class Plots(_SingletonSetting):
    """Plots setting."""

class XYPlots(_SingletonSetting):
    """XYPlots setting."""

class XYPlot(_CreatableNamedObjectSetting):
    """XYPlot setting."""

class Histogram(_SingletonSetting):
    """Histogram setting."""

class CumulativePlots(_SingletonSetting):
    """CumulativePlots setting."""

class CumulativePlot(_CreatableNamedObjectSetting):
    """CumulativePlot setting."""

class ProfileData(_SingletonSetting):
    """ProfileData setting."""

class InterpolatedData(_SingletonSetting):
    """InterpolatedData setting."""

class Scenes(_SingletonSetting):
    """Scenes setting."""

class Scene(_CreatableNamedObjectSetting):
    """Scene setting."""

class SceneAnimation(_SingletonSetting):
    """SceneAnimation setting."""

class Report(_SingletonSetting):
    """Report setting."""

class DiscretePhaseHistogram(_SingletonSetting):
    """DiscretePhaseHistogram setting."""

class Fluxes(_SingletonSetting):
    """Fluxes setting."""

class SurfaceIntegrals(_SingletonSetting):
    """SurfaceIntegrals setting."""

class VolumeIntegrals(_SingletonSetting):
    """VolumeIntegrals setting."""

class InputParameters(_SingletonSetting):
    """InputParameters setting."""

class OutputParameters(_SingletonSetting):
    """OutputParameters setting."""

class CustomFieldFunctions(_SingletonSetting):
    """CustomFieldFunctions setting."""

class CustomFieldFunction(_CreatableNamedObjectSetting):
    """CustomFieldFunction setting."""

class CustomVectors(_SingletonSetting):
    """CustomVectors setting."""

class CustomVector(_CreatableNamedObjectSetting):
    """CustomVector setting."""

class SimulationReports(_SingletonSetting):
    """SimulationReports setting."""

