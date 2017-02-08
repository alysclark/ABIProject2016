time = ['N', 'Y']

# Add Python bindings directory to PATH
import sys, os, math

# Set problem parameters
height = 1.0
width = 2.0
length = 3.0
diff_coeff = 0.225 # from readings
initial_conc = 0.5
start_time = 0.0
end_time = 1.0
exponent = 2
time_step = math.pow(1,exponent)
screen_output_freq = 2 # how many time steps between outputs to screen
steady_state_residual = []
time_residual = 0

(coordinateSystemUserNumber,
    regionUserNumber,
    basisUserNumber,
    generatedMeshUserNumber,
    meshUserNumber,
    decompositionUserNumber,
    geometricFieldUserNumber,
    equationsSetFieldUserNumber,
    dependentFieldUserNumber,
    materialFieldUserNumber,
    equationsSetUserNumber,
    problemUserNumber) = range(1,13)

numberGlobalXElements = 5
numberGlobalYElements = 5
numberGlobalZElements = 5

for time_idx in len(time):
    while steady_state_residual == [] or round(time_residual, 16) > steady_state_residual:  # 16 gives around 3dp accuracy

        if time == 'Y' and time_residual != 0:
            exponent -= 1
            time_step = math.pow(1, exponent)

        # Intialise OpenCMISS-Iron
        from opencmiss.iron import iron

        iron.DiagnosticsSetOn(iron.DiagnosticTypes.IN,[1,2,3,4,5],"Diagnostics",["DOMAIN_MAPPINGS_LOCAL_FROM_GLOBAL_CALCULATE"])

        # Get the computational nodes information
        numberOfComputationalNodes = iron.ComputationalNumberOfNodesGet()
        computationalNodeNumber = iron.ComputationalNodeNumberGet()

        # Create a RC coordinate system
        coordinateSystem = iron.CoordinateSystem()
        coordinateSystem.CreateStart(coordinateSystemUserNumber)
        coordinateSystem.dimension = 3
        coordinateSystem.CreateFinish()

        # Create a region
        region = iron.Region()
        region.CreateStart(regionUserNumber,iron.WorldRegion)
        region.label = "LaplaceRegion"
        region.coordinateSystem = coordinateSystem
        region.CreateFinish()

        # Create a tri-linear simplex basis
        basis = iron.Basis()
        basis.CreateStart(basisUserNumber)
        basis.TypeSet(iron.BasisTypes.SIMPLEX)
        basis.numberOfXi = 3
        basis.interpolationXi = [iron.BasisInterpolationSpecifications.LINEAR_SIMPLEX]*3
        basis.CreateFinish()

        # Create a generated mesh
        generatedMesh = iron.GeneratedMesh()
        generatedMesh.CreateStart(generatedMeshUserNumber,region)
        generatedMesh.type = iron.GeneratedMeshTypes.REGULAR
        generatedMesh.basis = [basis]
        generatedMesh.extent = [width,height,length]
        generatedMesh.numberOfElements = [numberGlobalXElements,numberGlobalYElements,numberGlobalZElements]

        mesh = iron.Mesh()
        generatedMesh.CreateFinish(meshUserNumber,mesh)

        # Create a decomposition for the mesh
        decomposition = iron.Decomposition()
        decomposition.CreateStart(decompositionUserNumber,mesh)
        decomposition.type = iron.DecompositionTypes.CALCULATED
        decomposition.numberOfDomains = numberOfComputationalNodes
        decomposition.CreateFinish()

        # Create a field for the geometry
        geometricField = iron.Field()
        geometricField.CreateStart(geometricFieldUserNumber,region)
        geometricField.meshDecomposition = decomposition
        geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,1,1)
        geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,2,1)
        geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,3,1)
        geometricField.CreateFinish()

        # Set geometry from the generated mesh
        generatedMesh.GeometricParametersCalculate(geometricField)

        # Create standard Laplace equations set
        equationsSetField = iron.Field()
        equationsSet = iron.EquationsSet()
        if time == 'Y':
            equationsSetSpecification = [iron.EquationsSetClasses.CLASSICAL_FIELD,
                    iron.EquationsSetTypes.DIFFUSION_EQUATION,
                    iron.EquationsSetSubtypes.NO_SOURCE_DIFFUSION]
        else:
            equationsSetSpecification = [iron.EquationsSetClasses.CLASSICAL_FIELD,
                    iron.EquationsSetTypes.LAPLACE_EQUATION,
                    iron.EquationsSetSubtypes.STANDARD_LAPLACE]

        equationsSet.CreateStart(equationsSetUserNumber,region,geometricField,
                equationsSetSpecification,equationsSetFieldUserNumber,equationsSetField)
        equationsSet.CreateFinish()

        # Create dependent field
        dependentField = iron.Field()
        equationsSet.DependentCreateStart(dependentFieldUserNumber,dependentField)
        dependentField.DOFOrderTypeSet(iron.FieldVariableTypes.U,iron.FieldDOFOrderTypes.SEPARATED)
        dependentField.DOFOrderTypeSet(iron.FieldVariableTypes.DELUDELN,iron.FieldDOFOrderTypes.SEPARATED)
        equationsSet.DependentCreateFinish()

        if time == 'Y':
            # Create material field
            materialField = iron.Field()
            equationsSet.MaterialsCreateStart(materialFieldUserNumber,materialField)

            # Sets the material field component number
            materialField.ComponentMeshComponentSet(iron.FieldVariableTypes.U, 1, 1)
            materialField.ComponentMeshComponentSet(iron.FieldVariableTypes.U, 2, 1)
            materialField.ComponentMeshComponentSet(iron.FieldVariableTypes.U, 3, 1)

            # Change to nodal based interpolation
            materialField.ComponentInterpolationSet(iron.FieldVariableTypes.U,1,iron.FieldInterpolationTypes.NODE_BASED)
            materialField.ComponentInterpolationSet(iron.FieldVariableTypes.U,2,iron.FieldInterpolationTypes.NODE_BASED)
            materialField.ComponentInterpolationSet(iron.FieldVariableTypes.U,3,iron.FieldInterpolationTypes.NODE_BASED)

            equationsSet.MaterialsCreateFinish()

            # Changing diffusion coefficient
            materialField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1,diff_coeff)
            materialField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,2,diff_coeff)
            materialField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,3,diff_coeff)

            # Initialise dependent field
            dependentField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1,initial_conc)

        else:
            # Initialise dependent field
            dependentField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1,0.5)

        # Create equations
        equations = iron.Equations()
        equationsSet.EquationsCreateStart(equations)
        equations.sparsityType = iron.EquationsSparsityTypes.SPARSE
        equations.outputType = iron.EquationsOutputTypes.NONE
        equationsSet.EquationsCreateFinish()

        if time == 'Y':
            # Create problem
            problem = iron.Problem()
            problemSpecification = [iron.ProblemClasses.CLASSICAL_FIELD,
                iron.ProblemTypes.DIFFUSION_EQUATION,
                iron.ProblemSubtypes.NO_SOURCE_DIFFUSION]
            problem.CreateStart(problemUserNumber, problemSpecification)
            problem.CreateFinish()

            # Create control loops
            problem.ControlLoopCreateStart()
            controlLoop = iron.ControlLoop()
            problem.ControlLoopGet([iron.ControlLoopIdentifiers.NODE], controlLoop)
            controlLoop.TimesSet(start_time, end_time, time_step)
            controlLoop.TimeOutputSet(screen_output_freq)
            problem.ControlLoopCreateFinish()

            # Create problem solver
            dynamicSolver = iron.Solver()
            problem.SolversCreateStart()
            problem.SolverGet([iron.ControlLoopIdentifiers.NODE], 1, dynamicSolver)
            dynamicSolver.outputType = iron.SolverOutputTypes.PROGRESS
            linearSolver = iron.Solver()
            dynamicSolver.DynamicLinearSolverGet(linearSolver)
            linearSolver.outputType = iron.SolverOutputTypes.NONE
            linearSolver.linearType = iron.LinearSolverTypes.ITERATIVE
            linearSolver.LinearIterativeMaximumIterationsSet(1000)

        else:
            problem = iron.Problem()
            problemSpecification = [iron.ProblemClasses.CLASSICAL_FIELD,
                iron.ProblemTypes.LAPLACE_EQUATION,
                iron.ProblemSubtypes.STANDARD_LAPLACE]
            problem.CreateStart(problemUserNumber, problemSpecification)
            problem.CreateFinish()

            problem.ControlLoopCreateStart()
            problem.ControlLoopCreateFinish()

            solver = iron.Solver()
            problem.SolversCreateStart()
            problem.SolverGet([iron.ControlLoopIdentifiers.NODE],1,solver)
            solver.outputType = iron.SolverOutputTypes.SOLVER
            solver.linearType = iron.LinearSolverTypes.ITERATIVE
            solver.linearIterativeAbsoluteTolerance = 1.0E-12
            solver.linearIterativeRelativeTolerance = 1.0E-12
            problem.SolversCreateFinish()

        # Create solver equations and add equations set to solver equations
        solver = iron.Solver()
        solverEquations = iron.SolverEquations()
        problem.SolverEquationsCreateStart()
        problem.SolverGet([iron.ControlLoopIdentifiers.NODE],1,solver)
        solver.SolverEquationsGet(solverEquations)
        solverEquations.sparsityType = iron.SolverEquationsSparsityTypes.SPARSE
        equationsSetIndex = solverEquations.EquationsSetAdd(equationsSet)
        problem.SolverEquationsCreateFinish()

        # Create boundary conditions and set first and last nodes to 0.0 and 1.0
        boundaryConditions = iron.BoundaryConditions()
        solverEquations.BoundaryConditionsCreateStart(boundaryConditions)
        firstNodeNumber=1
        nodes = iron.Nodes()
        region.NodesGet(nodes)
        lastNodeNumber = nodes.numberOfNodes
        firstNodeDomain = decomposition.NodeDomainGet(firstNodeNumber,1)
        lastNodeDomain = decomposition.NodeDomainGet(lastNodeNumber,1)
        if firstNodeDomain == computationalNodeNumber:
            boundaryConditions.SetNode(dependentField,iron.FieldVariableTypes.U,1,1,firstNodeNumber,1,iron.BoundaryConditionsTypes.FIXED,0.0)
        if lastNodeDomain == computationalNodeNumber:
            boundaryConditions.SetNode(dependentField,iron.FieldVariableTypes.U,1,1,lastNodeNumber,1,iron.BoundaryConditionsTypes.FIXED,1.0)
        solverEquations.BoundaryConditionsCreateFinish()

        # Solve the problem
        problem.Solve()

        if time == 'N':
            steady_state_residual = problem_output

        if time == 'Y' and round(time_residual, 16) <= steady_state_residual:

            # Export results as fml files
            baseName = "laplace"
            dataFormat = "PLAIN_TEXT"
            fml = iron.FieldMLIO()
            fml.OutputCreate(mesh, "", baseName, dataFormat)
            fml.OutputAddFieldNoType(baseName + ".geometric", dataFormat, geometricField,
                                     iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES)
            fml.OutputAddFieldNoType(baseName + ".phi", dataFormat, dependentField,
                                     iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES)
            fml.OutputWrite("SimplexIterative.xml")
            fml.Finalise()

            # Export results
            fields = iron.Fields()
            fields.CreateRegion(region)
            fields.NodesExport("SimplexIterativeResults", "FORTRAN")
            fields.ElementsExport("SimplexIterativeResults", "FORTRAN")
            fields.Finalise()

        iron.Finalise()