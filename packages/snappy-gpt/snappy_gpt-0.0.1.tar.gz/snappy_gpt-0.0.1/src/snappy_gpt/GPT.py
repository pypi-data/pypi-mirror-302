from esa_snappy import HashMap, GPF

class Node:
    def __init__(self, name):
        self.name=name
        self.alias=''.join([c for c in name if c.isupper()])
        if len(self.alias)<2:
            self.alias.join(name[1])
        if len(self.alias)<3:
            self.alias.join(name[2])
        self.parameters = HashMap()
    
    def put(self, paramName, paramValue):
        self.parameters.put(paramName, paramValue)

    def get_name(self):
        return self.name
    
    def get_parameter(self):
        return self.parameters
    
    def get_alias(self):
        return self.alias

class Graph:
    def __init__(self):
        self.nodes = []
        return
    
    def create_product(self, product=None, outFile=None, fileFormat='BEAM-DIMAP'):
        name=outFile
        if product==None and self.nodes[0].get_name()=='Read':
            node=self.nodes[0]
            product=GPF.createProduct(node.get_name(), node.get_parameter())
            self.nodes=self.nodes[1:]
        for node in self.nodes:
            name = f"{name}_{node.get_alias()}"
            product=GPF.createProduct(node.get_name(), node.get_parameter(), product)
        
        if outFile:
            GPF.writeProduct(product, name , fileFormat, incremental=False)

        return product
    
    def add_gemi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        This retrieves the Global Environmental Monitoring Index (GEMI).

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the RED source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the GEMI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the GEMI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('GemiOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_decision_tree(self,
        decisionTree = None
        ):
        '''
        Perform decision tree classification

        Parameters
        ----------
        decisionTree : org.esa.s1tbx.fex.gpf.decisiontree.DecisionTreeNode[]
        '''

        node = Node('DecisionTree')

        if decisionTree:
            node.put('decisionTree', decisionTree)

        self.nodes.append(node)

    def add_land_sea_mask(self,
        sourceBandNames = None,
        landMask = None,
        useSRTM = None,
        geometry = None,
        invertGeometry = None,
        shorelineExtension = None
        ):
        '''
        Creates a bitmask defining land vs ocean.

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        landMask : java.lang.Boolean
            Default 'true'
        useSRTM : java.lang.Boolean
            Default 'true'
        geometry : java.lang.String
        invertGeometry : java.lang.Boolean
            Default 'false'
        shorelineExtension : java.lang.Integer
            Default '0'
        '''

        node = Node('Land-Sea-Mask')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if landMask:
            node.put('landMask', landMask)
        if useSRTM:
            node.put('useSRTM', useSRTM)
        if geometry:
            node.put('geometry', geometry)
        if invertGeometry:
            node.put('invertGeometry', invertGeometry)
        if shorelineExtension:
            node.put('shorelineExtension', shorelineExtension)

        self.nodes.append(node)

    def add_calibration(self,
        sourceBandNames = None,
        auxFile = None,
        externalAuxFile = None,
        outputImageInComplex = None,
        outputImageScaleInDb = None,
        createGammaBand = None,
        createBetaBand = None,
        selectedPolarisations = None,
        outputSigmaBand = None,
        outputGammaBand = None,
        outputBetaBand = None
        ):
        '''
        Calibration of products

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        auxFile : java.lang.String, ['Latest Auxiliary File', 'Product Auxiliary File', 'External Auxiliary File']
            The auxiliary file
            Default 'Latest Auxiliary File'
        externalAuxFile : java.io.File
            The antenna elevation pattern gain auxiliary data file.
        outputImageInComplex : java.lang.Boolean
            Output image in complex
            Default 'false'
        outputImageScaleInDb : java.lang.Boolean
            Output image scale
            Default 'false'
        createGammaBand : java.lang.Boolean
            Create gamma0 virtual band
            Default 'false'
        createBetaBand : java.lang.Boolean
            Create beta0 virtual band
            Default 'false'
        selectedPolarisations : java.lang.String[]
            The list of polarisations
        outputSigmaBand : java.lang.Boolean
            Output sigma0 band
            Default 'true'
        outputGammaBand : java.lang.Boolean
            Output gamma0 band
            Default 'false'
        outputBetaBand : java.lang.Boolean
            Output beta0 band
            Default 'false'
        '''

        node = Node('Calibration')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if auxFile:
            node.put('auxFile', auxFile)
        if externalAuxFile:
            node.put('externalAuxFile', externalAuxFile)
        if outputImageInComplex:
            node.put('outputImageInComplex', outputImageInComplex)
        if outputImageScaleInDb:
            node.put('outputImageScaleInDb', outputImageScaleInDb)
        if createGammaBand:
            node.put('createGammaBand', createGammaBand)
        if createBetaBand:
            node.put('createBetaBand', createBetaBand)
        if selectedPolarisations:
            node.put('selectedPolarisations', selectedPolarisations)
        if outputSigmaBand:
            node.put('outputSigmaBand', outputSigmaBand)
        if outputGammaBand:
            node.put('outputGammaBand', outputGammaBand)
        if outputBetaBand:
            node.put('outputBetaBand', outputBetaBand)

        self.nodes.append(node)

    def add_ndwi2_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        greenFactor: float = None,
        nirFactor: float = None,
        greenSourceBand = None,
        nirSourceBand = None
        ):
        '''
        The Normalized Difference Water Index, allowing for the measurement of surface water extent

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        greenFactor : float
            The value of the green source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        greenSourceBand : java.lang.String
            The green band for the NDWI2 computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the NDWI2 computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('Ndwi2Op')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if greenFactor:
            node.put('greenFactor', greenFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if greenSourceBand:
            node.put('greenSourceBand', greenSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_wdvi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        slopeSoilLine: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        Weighted Difference Vegetation Index retrieves the Isovegetation lines parallel to soil line.
Soil line has an arbitrary slope and passes through origin

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        slopeSoilLine : float
            Soil line has an arbitrary slope and passes through origin
            Default '1.5F'
        redSourceBand : java.lang.String
            The red band for the WDVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the WDVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('WdviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if slopeSoilLine:
            node.put('slopeSoilLine', slopeSoilLine)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_import_vector(self,
        vectorFile = None,
        separateShapes: bool = None
        ):
        '''
        Imports a shape file into a product

        Parameters
        ----------
        vectorFile : java.io.File
        separateShapes : boolean
            Default 'true'
        '''

        node = Node('Import-Vector')

        if vectorFile:
            node.put('vectorFile', vectorFile)
        if separateShapes:
            node.put('separateShapes', separateShapes)

        self.nodes.append(node)

    def add_set_no_data_value(self,
        noDataValueUsed = None,
        noDataValue: float = None
        ):
        '''
        Set NoDataValueUsed flag and NoDataValue for all bands

        Parameters
        ----------
        noDataValueUsed : java.lang.Boolean
            Default 'true'
        noDataValue : double
            Default '0.0'
        '''

        node = Node('SetNoDataValue')

        if noDataValueUsed:
            node.put('noDataValueUsed', noDataValueUsed)
        if noDataValue:
            node.put('noDataValue', noDataValue)

        self.nodes.append(node)

    def add_slice_assembly(self,
        selectedPolarisations = None
        ):
        '''
        Merges Sentinel-1 slice products

        Parameters
        ----------
        selectedPolarisations : java.lang.String[]
            The list of polarisations
        '''

        node = Node('SliceAssembly')

        if selectedPolarisations:
            node.put('selectedPolarisations', selectedPolarisations)

        self.nodes.append(node)

    def add_generic_region_merging_op(self,
        mergingCostCriterion = None,
        regionMergingCriterion = None,
        totalIterationsForSecondSegmentation: int = None,
        threshold: float = None,
        spectralWeight: float = None,
        shapeWeight: float = None,
        sourceBandNames = None
        ):
        '''
        The 'Generic Region Merging' operator computes the distinct regions from a product

        Parameters
        ----------
        mergingCostCriterion : java.lang.String, ['Spring', 'Baatz & Schape', 'Full Lamda Schedule']
            The method to compute the region merging.
            Default 'Baatz & Schape'
        regionMergingCriterion : java.lang.String, ['Best Fitting', 'Local Mutual Best Fitting']
            The method to check the region merging.
            Default 'Local Mutual Best Fitting'
        totalIterationsForSecondSegmentation : int
            The total number of iterations.
            Default '50'
        threshold : float
            The threshold.
            Default '100.0'
        spectralWeight : float
            The spectral weight.
            Default '0.5'
        shapeWeight : float
            The shape weight.
            Default '0.5'
        sourceBandNames : java.lang.String[]
            The source bands for the computation.
        '''

        node = Node('GenericRegionMergingOp')

        if mergingCostCriterion:
            node.put('mergingCostCriterion', mergingCostCriterion)
        if regionMergingCriterion:
            node.put('regionMergingCriterion', regionMergingCriterion)
        if totalIterationsForSecondSegmentation:
            node.put('totalIterationsForSecondSegmentation', totalIterationsForSecondSegmentation)
        if threshold:
            node.put('threshold', threshold)
        if spectralWeight:
            node.put('spectralWeight', spectralWeight)
        if shapeWeight:
            node.put('shapeWeight', shapeWeight)
        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)

        self.nodes.append(node)

    def addc2rcc_landsat7(self,
        validPixelExpression = None,
        salinity: float = None,
        temperature: float = None,
        ozone: float = None,
        press: float = None,
        elevation: float = None,
        TSMfakBpart: float = None,
        TSMfakBwit: float = None,
        CHLexp: float = None,
        CHLfak: float = None,
        thresholdRtosaOOS: float = None,
        thresholdAcReflecOos: float = None,
        thresholdCloudTDown835: float = None,
        atmosphericAuxDataPath = None,
        alternativeNNPath = None,
        outputAsRrs: bool = None,
        deriveRwFromPathAndTransmittance: bool = None,
        outputRtoa: bool = None,
        outputRtosaGc: bool = None,
        outputRtosaGcAann: bool = None,
        outputRpath: bool = None,
        outputTdown: bool = None,
        outputTup: bool = None,
        outputAcReflectance: bool = None,
        outputRhown: bool = None,
        outputOos: bool = None,
        outputKd: bool = None,
        outputUncertainties: bool = None
        ):
        '''
        Performs atmospheric correction and IOP retrieval with uncertainties on Landsat-7 L1 data products.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Defines the pixels which are valid for processing.
        salinity : double
            The value used as salinity for the scene.
            Default '35.0'
        temperature : double
            The value used as temperature for the scene.
            Default '15.0'
        ozone : double
            The value used as ozone if not provided by auxiliary data.
            Default '330'
        press : double
            The surface air pressure at sea level if not provided by auxiliary data.
            Default '1000'
        elevation : double
            Used as fallback if elevation could not be taken from GETASSE30 DEM.
            Default '0'
        TSMfakBpart : double
            TSM factor (TSM = TSMfac * iop_btot^TSMexp).
            Default '1.72'
        TSMfakBwit : double
            TSM exponent (TSM = TSMfac * iop_btot^TSMexp).
            Default '3.1'
        CHLexp : double
            Chlorophyll exponent ( CHL = iop_apig^CHLexp * CHLfac).
            Default '1.04'
        CHLfak : double
            Chlorophyll factor ( CHL = iop_apig^CHLexp * CHLfac).
            Default '21.0'
        thresholdRtosaOOS : double
            Threshold for out of scope of nn training dataset flag for gas corrected top-of-atmosphere reflectances.
            Default '0.05'
        thresholdAcReflecOos : double
            Threshold for out of scope of nn training dataset flag for atmospherically corrected reflectances.
            Default '0.1'
        thresholdCloudTDown835 : double
            Threshold for cloud test based on downwelling transmittance @835.
            Default '0.955'
        atmosphericAuxDataPath : java.lang.String
            Path to the atmospheric auxiliary data directory. Use either this or the specified products on the I/O Parameters tab. If the auxiliary data is not available at this path, the data will automatically be downloaded.
        alternativeNNPath : java.lang.String
            Path to an alternative set of neuronal nets. Use this to replace the standard set of neuronal nets.
        outputAsRrs : boolean
            Write remote sensing reflectances instead of water leaving reflectances.
            Default 'false'
        deriveRwFromPathAndTransmittance : boolean
            Alternative way of calculating water reflectance. Still experimental.
            Default 'false'
        outputRtoa : boolean
            Default 'true'
        outputRtosaGc : boolean
            Default 'false'
        outputRtosaGcAann : boolean
            Default 'false'
        outputRpath : boolean
            Default 'false'
        outputTdown : boolean
            Default 'false'
        outputTup : boolean
            Default 'false'
        outputAcReflectance : boolean
            Default 'true'
        outputRhown : boolean
            Default 'true'
        outputOos : boolean
            Default 'false'
        outputKd : boolean
            Default 'true'
        outputUncertainties : boolean
            Default 'true'
        '''

        node = Node('c2rcc.landsat7')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if salinity:
            node.put('salinity', salinity)
        if temperature:
            node.put('temperature', temperature)
        if ozone:
            node.put('ozone', ozone)
        if press:
            node.put('press', press)
        if elevation:
            node.put('elevation', elevation)
        if TSMfakBpart:
            node.put('TSMfakBpart', TSMfakBpart)
        if TSMfakBwit:
            node.put('TSMfakBwit', TSMfakBwit)
        if CHLexp:
            node.put('CHLexp', CHLexp)
        if CHLfak:
            node.put('CHLfak', CHLfak)
        if thresholdRtosaOOS:
            node.put('thresholdRtosaOOS', thresholdRtosaOOS)
        if thresholdAcReflecOos:
            node.put('thresholdAcReflecOos', thresholdAcReflecOos)
        if thresholdCloudTDown835:
            node.put('thresholdCloudTDown835', thresholdCloudTDown835)
        if atmosphericAuxDataPath:
            node.put('atmosphericAuxDataPath', atmosphericAuxDataPath)
        if alternativeNNPath:
            node.put('alternativeNNPath', alternativeNNPath)
        if outputAsRrs:
            node.put('outputAsRrs', outputAsRrs)
        if deriveRwFromPathAndTransmittance:
            node.put('deriveRwFromPathAndTransmittance', deriveRwFromPathAndTransmittance)
        if outputRtoa:
            node.put('outputRtoa', outputRtoa)
        if outputRtosaGc:
            node.put('outputRtosaGc', outputRtosaGc)
        if outputRtosaGcAann:
            node.put('outputRtosaGcAann', outputRtosaGcAann)
        if outputRpath:
            node.put('outputRpath', outputRpath)
        if outputTdown:
            node.put('outputTdown', outputTdown)
        if outputTup:
            node.put('outputTup', outputTup)
        if outputAcReflectance:
            node.put('outputAcReflectance', outputAcReflectance)
        if outputRhown:
            node.put('outputRhown', outputRhown)
        if outputOos:
            node.put('outputOos', outputOos)
        if outputKd:
            node.put('outputKd', outputKd)
        if outputUncertainties:
            node.put('outputUncertainties', outputUncertainties)

        self.nodes.append(node)

    def addc2rcc_seawifs(self,
        validPixelExpression = None,
        salinity: float = None,
        temperature: float = None,
        ozone: float = None,
        press: float = None,
        atmosphericAuxDataPath = None,
        outputRtosa: bool = None,
        outputAsRrs: bool = None
        ):
        '''
        Performs atmospheric correction and IOP retrieval on SeaWifs L1C data products.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Defines the pixels which are valid for processing
            Default '!(l2_flags.LAND || rhot_865 > 0.25)'
        salinity : double
            The value used as salinity for the scene
            Default '35.0'
        temperature : double
            The value used as temperature for the scene
            Default '15.0'
        ozone : double
            The value used as ozone if not provided by auxiliary data
            Default '330'
        press : double
            The surface air pressure at sea level if not provided by auxiliary data
            Default '1000'
        atmosphericAuxDataPath : java.lang.String
            Path to the atmospheric auxiliary data directory. Use either this or tomsomiStartProduct, tomsomiEndProduct, ncepStartProduct and ncepEndProduct to use ozone and air pressure aux data for calculations. If the auxiliary data needed for interpolation not available in this path, the data will automatically downloaded.
        outputRtosa : boolean
            Default 'false'
        outputAsRrs : boolean
            Reflectance values in the target product shall be either written as remote sensing or water leaving reflectances
            Default 'false'
        '''

        node = Node('c2rcc.seawifs')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if salinity:
            node.put('salinity', salinity)
        if temperature:
            node.put('temperature', temperature)
        if ozone:
            node.put('ozone', ozone)
        if press:
            node.put('press', press)
        if atmosphericAuxDataPath:
            node.put('atmosphericAuxDataPath', atmosphericAuxDataPath)
        if outputRtosa:
            node.put('outputRtosa', outputRtosa)
        if outputAsRrs:
            node.put('outputAsRrs', outputAsRrs)

        self.nodes.append(node)

    def add_meris_combined_cloud(self,
        copyAllTiePoints: bool = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        '''

        node = Node('Meris.CombinedCloud')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)

        self.nodes.append(node)

    def add_tsavi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        slope: float = None,
        intercept: float = None,
        adjustment: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        This retrieves the Transformed Soil Adjusted Vegetation Index (TSAVI).

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the RED source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        slope : float
            The soil line slope.
            Default '0.5F'
        intercept : float
            The soil line intercept.
            Default '0.5F'
        adjustment : float
            Adjustment factor to minimize soil background.
            Default '0.08F'
        redSourceBand : java.lang.String
            The red band for the TSAVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the TSAVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('TsaviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if slope:
            node.put('slope', slope)
        if intercept:
            node.put('intercept', intercept)
        if adjustment:
            node.put('adjustment', adjustment)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_l3to_l1(self,
        copyAllTiePoints: bool = None,
        maskBand = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        maskBand : java.lang.String
        '''

        node = Node('L3ToL1')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if maskBand:
            node.put('maskBand', maskBand)

        self.nodes.append(node)

    def add_three_pass_din_sar(self,
        orbitDegree: int = None
        ):
        '''
        Differential Interferometry

        Parameters
        ----------
        orbitDegree : int
            Degree of orbit interpolation polynomial
            Default '3'
        '''

        node = Node('Three-passDInSAR')

        if orbitDegree:
            node.put('orbitDegree', orbitDegree)

        self.nodes.append(node)

    def add_meris_cloud_probability(self,
        copyAllTiePoints: bool = None,
        configFile = None,
        validLandExpression = None,
        validOceanExpression = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        configFile : java.lang.String
        validLandExpression : java.lang.String
        validOceanExpression : java.lang.String
        '''

        node = Node('Meris.CloudProbability')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if configFile:
            node.put('configFile', configFile)
        if validLandExpression:
            node.put('validLandExpression', validLandExpression)
        if validOceanExpression:
            node.put('validOceanExpression', validOceanExpression)

        self.nodes.append(node)

    def add_eap_phase_correction(self
        ):
        '''
        EAP Phase Correction

        Parameters
        ----------
        '''

        node = Node('EAP-Phase-Correction')


        self.nodes.append(node)

    def add_meris_cloud_classification(self,
        copyAllTiePoints: bool = None,
        l2Pressures: bool = None,
        l2CloudDetection: bool = None
        ):
        '''
        MERIS L2 cloud classification.

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        l2Pressures : boolean
            If 'true' the algorithm will compute L2 Pressures.
            Default 'true'
        l2CloudDetection : boolean
            If 'true' the algorithm will compute L2 Cloud detection flags.
            Default 'true'
        '''

        node = Node('Meris.CloudClassification')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if l2Pressures:
            node.put('l2Pressures', l2Pressures)
        if l2CloudDetection:
            node.put('l2CloudDetection', l2CloudDetection)

        self.nodes.append(node)

    def add_meris_cloud_shadow(self,
        copyAllTiePoints: bool = None,
        shadowWidth: int = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        shadowWidth : int
        '''

        node = Node('Meris.CloudShadow')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if shadowWidth:
            node.put('shadowWidth', shadowWidth)

        self.nodes.append(node)

    def add_interferogram(self,
        subtractFlatEarthPhase: bool = None,
        srpPolynomialDegree: int = None,
        srpNumberPoints: int = None,
        orbitDegree: int = None,
        includeCoherence: bool = None,
        cohWinAz: int = None,
        cohWinRg: int = None,
        squarePixel = None,
        subtractTopographicPhase: bool = None,
        demName = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        externalDEMApplyEGM = None,
        tileExtensionPercent = None,
        outputElevation: bool = None,
        outputLatLon: bool = None
        ):
        '''
        Compute interferograms from stack of coregistered S-1 images

        Parameters
        ----------
        subtractFlatEarthPhase : boolean
            Default 'true'
        srpPolynomialDegree : int, ['1', '2', '3', '4', '5', '6', '7', '8']
            Order of 'Flat earth phase' polynomial
            Default '5'
        srpNumberPoints : int, ['301', '401', '501', '601', '701', '801', '901', '1001']
            Number of points for the 'flat earth phase' polynomial estimation
            Default '501'
        orbitDegree : int, ['1', '2', '3', '4', '5']
            Degree of orbit (polynomial) interpolator
            Default '3'
        includeCoherence : boolean
            Default 'true'
        cohWinAz : int
            Size of coherence estimation window in Azimuth direction
            Default '10'
        cohWinRg : int
            Size of coherence estimation window in Range direction
            Default '10'
        squarePixel : java.lang.Boolean
            Use ground square pixel
            Default 'true'
        subtractTopographicPhase : boolean
            Default 'false'
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        externalDEMApplyEGM : java.lang.Boolean
            Default 'true'
        tileExtensionPercent : java.lang.String
            Define extension of tile for DEM simulation (optimization parameter).
            Default '100'
        outputElevation : boolean
            Default 'false'
        outputLatLon : boolean
            Default 'false'
        '''

        node = Node('Interferogram')

        if subtractFlatEarthPhase:
            node.put('subtractFlatEarthPhase', subtractFlatEarthPhase)
        if srpPolynomialDegree:
            node.put('srpPolynomialDegree', srpPolynomialDegree)
        if srpNumberPoints:
            node.put('srpNumberPoints', srpNumberPoints)
        if orbitDegree:
            node.put('orbitDegree', orbitDegree)
        if includeCoherence:
            node.put('includeCoherence', includeCoherence)
        if cohWinAz:
            node.put('cohWinAz', cohWinAz)
        if cohWinRg:
            node.put('cohWinRg', cohWinRg)
        if squarePixel:
            node.put('squarePixel', squarePixel)
        if subtractTopographicPhase:
            node.put('subtractTopographicPhase', subtractTopographicPhase)
        if demName:
            node.put('demName', demName)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if externalDEMApplyEGM:
            node.put('externalDEMApplyEGM', externalDEMApplyEGM)
        if tileExtensionPercent:
            node.put('tileExtensionPercent', tileExtensionPercent)
        if outputElevation:
            node.put('outputElevation', outputElevation)
        if outputLatLon:
            node.put('outputLatLon', outputLatLon)

        self.nodes.append(node)

    def add_polarimetric_parameters(self,
        useMeanMatrix: bool = None,
        windowSizeXStr = None,
        windowSizeYStr = None,
        outputSpan: bool = None,
        outputPedestalHeight: bool = None,
        outputRVI: bool = None,
        outputRFDI: bool = None,
        outputCSI: bool = None,
        outputVSI: bool = None,
        outputBMI: bool = None,
        outputITI: bool = None,
        outputHHVVRatio: bool = None,
        outputHHHVRatio: bool = None,
        outputVVVHRatio: bool = None
        ):
        '''
        Compute general polarimetric parameters

        Parameters
        ----------
        useMeanMatrix : boolean
            Use mean coherency or covariance matrix
            Default 'true'
        windowSizeXStr : java.lang.String, ['3', '5', '7', '9', '11', '13', '15', '17', '19']
            Default '5'
        windowSizeYStr : java.lang.String, ['3', '5', '7', '9', '11', '13', '15', '17', '19']
            Default '5'
        outputSpan : boolean
            Output Span
            Default 'true'
        outputPedestalHeight : boolean
            Output pedestal height
            Default 'false'
        outputRVI : boolean
            Output RVI
            Default 'false'
        outputRFDI : boolean
            Output RFDI
            Default 'false'
        outputCSI : boolean
            Output CSI
            Default 'false'
        outputVSI : boolean
            Output VSI
            Default 'false'
        outputBMI : boolean
            Output BMI
            Default 'false'
        outputITI : boolean
            Output ITI
            Default 'false'
        outputHHVVRatio : boolean
            Output Co-Pol HH/VV
            Default 'false'
        outputHHHVRatio : boolean
            Output Cross-Pol HH/HV
            Default 'false'
        outputVVVHRatio : boolean
            Output Cross-Pol VV/VH
            Default 'false'
        '''

        node = Node('Polarimetric-Parameters')

        if useMeanMatrix:
            node.put('useMeanMatrix', useMeanMatrix)
        if windowSizeXStr:
            node.put('windowSizeXStr', windowSizeXStr)
        if windowSizeYStr:
            node.put('windowSizeYStr', windowSizeYStr)
        if outputSpan:
            node.put('outputSpan', outputSpan)
        if outputPedestalHeight:
            node.put('outputPedestalHeight', outputPedestalHeight)
        if outputRVI:
            node.put('outputRVI', outputRVI)
        if outputRFDI:
            node.put('outputRFDI', outputRFDI)
        if outputCSI:
            node.put('outputCSI', outputCSI)
        if outputVSI:
            node.put('outputVSI', outputVSI)
        if outputBMI:
            node.put('outputBMI', outputBMI)
        if outputITI:
            node.put('outputITI', outputITI)
        if outputHHVVRatio:
            node.put('outputHHVVRatio', outputHHVVRatio)
        if outputHHHVRatio:
            node.put('outputHHHVRatio', outputHHHVRatio)
        if outputVVVHRatio:
            node.put('outputVVVHRatio', outputVVVHRatio)

        self.nodes.append(node)

    def add_meris_sdr(self,
        copyAllTiePoints: bool = None,
        neuralNetFile = None,
        validBandName = None,
        aot470Name = None,
        angName = None,
        angValue: float = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        neuralNetFile : java.lang.String
        validBandName : java.lang.String
        aot470Name : java.lang.String
        angName : java.lang.String
        angValue : double
        '''

        node = Node('Meris.Sdr')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if neuralNetFile:
            node.put('neuralNetFile', neuralNetFile)
        if validBandName:
            node.put('validBandName', validBandName)
        if aot470Name:
            node.put('aot470Name', aot470Name)
        if angName:
            node.put('angName', angName)
        if angValue:
            node.put('angValue', angValue)

        self.nodes.append(node)

    def add_orientation_angle_correction(self,
        outputOrientationAngle: bool = None
        ):
        '''
        Perform polarization orientation angle correction for given coherency matrix

        Parameters
        ----------
        outputOrientationAngle : boolean
            Output Orientation Angle
            Default 'false'
        '''

        node = Node('Orientation-Angle-Correction')

        if outputOrientationAngle:
            node.put('outputOrientationAngle', outputOrientationAngle)

        self.nodes.append(node)

    def add_oil_spill_detection(self,
        sourceBandNames = None,
        backgroundWindowDim: float = None,
        k: float = None
        ):
        '''
        Detect oil spill.

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        backgroundWindowDim : double
            Background window dimension (km)
            Default '0.5'
        k : double
            Threshold shift from background mean
            Default '2.0'
        '''

        node = Node('Oil-Spill-Detection')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if backgroundWindowDim:
            node.put('backgroundWindowDim', backgroundWindowDim)
        if k:
            node.put('k', k)

        self.nodes.append(node)

    def add_flood_detection(self
        ):
        '''
        Detect flooded area.

        Parameters
        ----------
        '''

        node = Node('Flood-Detection')


        self.nodes.append(node)

    def add_sub_graph(self,
        graphFile = None
        ):
        '''
        Encapsulates a graph within a graph.

        Parameters
        ----------
        graphFile : java.io.File
        '''

        node = Node('SubGraph')

        if graphFile:
            node.put('graphFile', graphFile)

        self.nodes.append(node)

    def add_py_op(self,
        pythonModulePath = None,
        pythonModuleName = None,
        pythonClassName = None
        ):
        '''
        Uses Python code to process data products

        Parameters
        ----------
        pythonModulePath : java.lang.String
            Path to the Python module(s). Can be either an absolute path or relative to the current working directory.
            Default '.'
        pythonModuleName : java.lang.String
            Name of the Python module.
        pythonClassName : java.lang.String
            Name of the Python class which implements the operator. Please refer to the SNAP help for details.
        '''

        node = Node('PyOp')

        if pythonModulePath:
            node.put('pythonModulePath', pythonModulePath)
        if pythonModuleName:
            node.put('pythonModuleName', pythonModuleName)
        if pythonClassName:
            node.put('pythonClassName', pythonClassName)

        self.nodes.append(node)

    def add_collocate(self,
        sourceProductPaths = None,
        masterProductName = None,
        targetProductName = None,
        targetProductType = None,
        copySecondaryMetadata: bool = None,
        renameMasterComponents: bool = None,
        renameSlaveComponents: bool = None,
        masterComponentPattern = None,
        slaveComponentPattern = None,
        resamplingType = None
        ):
        '''
        Collocates two products based on their geo-codings.

        Parameters
        ----------
        sourceProductPaths : java.lang.String[]
            A comma-separated list of file paths specifying the source products
        masterProductName : java.lang.String
            The name of the master product.
        targetProductName : java.lang.String
            The name of the target product
            Default '_collocated'
        targetProductType : java.lang.String
            The product type string for the target product (informal)
            Default 'COLLOCATED'
        copySecondaryMetadata : boolean
            Copies also the metadata of the secondary (slave) products to the target
            Default 'false'
        renameMasterComponents : boolean
            Whether or not components of the master product shall be renamed in the target product.
            Default 'true'
        renameSlaveComponents : boolean
            Whether or not components of the slave product shall be renamed in the target product.
            Default 'true'
        masterComponentPattern : java.lang.String
            The text pattern to be used when renaming master components.
            Default '${ORIGINAL_NAME}_M'
        slaveComponentPattern : java.lang.String
            The text pattern to be used when renaming slave components.
            Default '${ORIGINAL_NAME}_S${SLAVE_NUMBER_ID}'
        resamplingType : org.esa.snap.collocation.ResamplingType
            The method to be used when resampling the slave grid onto the master grid.
            Default 'NEAREST_NEIGHBOUR'
        '''

        node = Node('Collocate')

        if sourceProductPaths:
            node.put('sourceProductPaths', sourceProductPaths)
        if masterProductName:
            node.put('masterProductName', masterProductName)
        if targetProductName:
            node.put('targetProductName', targetProductName)
        if targetProductType:
            node.put('targetProductType', targetProductType)
        if copySecondaryMetadata:
            node.put('copySecondaryMetadata', copySecondaryMetadata)
        if renameMasterComponents:
            node.put('renameMasterComponents', renameMasterComponents)
        if renameSlaveComponents:
            node.put('renameSlaveComponents', renameSlaveComponents)
        if masterComponentPattern:
            node.put('masterComponentPattern', masterComponentPattern)
        if slaveComponentPattern:
            node.put('slaveComponentPattern', slaveComponentPattern)
        if resamplingType:
            node.put('resamplingType', resamplingType)

        self.nodes.append(node)

    def add_fill_dem_hole(self,
        sourceBands = None,
        NoDataValue = None
        ):
        '''
        Fill holes in given DEM product file.

        Parameters
        ----------
        sourceBands : java.lang.String[]
            The list of source bands.
        NoDataValue : java.lang.Double
            Default '0.0'
        '''

        node = Node('Fill-DEM-Hole')

        if sourceBands:
            node.put('sourceBands', sourceBands)
        if NoDataValue:
            node.put('NoDataValue', NoDataValue)

        self.nodes.append(node)

    def add_ndti_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        greenFactor: float = None,
        redSourceBand = None,
        greenSourceBand = None
        ):
        '''
        Normalized difference turbidity index, allowing for the measurement of water turbidity

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        greenFactor : float
            The value of the green source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the NDTI computation. If not provided, the operator will try to find the best fitting band.
        greenSourceBand : java.lang.String
            The green band for the NDTI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('NdtiOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if greenFactor:
            node.put('greenFactor', greenFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if greenSourceBand:
            node.put('greenSourceBand', greenSourceBand)

        self.nodes.append(node)

    def add_fill_aerosol(self,
        copyAllTiePoints: bool = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        '''

        node = Node('FillAerosol')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)

        self.nodes.append(node)

    def add_topo_phase_removal(self,
        orbitDegree: int = None,
        demName = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        tileExtensionPercent = None,
        outputTopoPhaseBand = None,
        outputElevationBand = None,
        outputLatLonBands = None
        ):
        '''
        Compute and subtract TOPO phase

        Parameters
        ----------
        orbitDegree : int
            Degree of orbit interpolation polynomial
            Default '3'
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        tileExtensionPercent : java.lang.String
            Define extension of tile for DEM simulation (optimization parameter).
            Default '100'
        outputTopoPhaseBand : java.lang.Boolean
            Output topographic phase band.
            Default 'false'
        outputElevationBand : java.lang.Boolean
            Output elevation band.
            Default 'false'
        outputLatLonBands : java.lang.Boolean
            Output lat/lon bands.
            Default 'false'
        '''

        node = Node('TopoPhaseRemoval')

        if orbitDegree:
            node.put('orbitDegree', orbitDegree)
        if demName:
            node.put('demName', demName)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if tileExtensionPercent:
            node.put('tileExtensionPercent', tileExtensionPercent)
        if outputTopoPhaseBand:
            node.put('outputTopoPhaseBand', outputTopoPhaseBand)
        if outputElevationBand:
            node.put('outputElevationBand', outputElevationBand)
        if outputLatLonBands:
            node.put('outputLatLonBands', outputLatLonBands)

        self.nodes.append(node)

    def add_reproject(self,
        wktFile = None,
        crs = None,
        resamplingName = None,
        referencePixelX = None,
        referencePixelY = None,
        easting = None,
        northing = None,
        orientation = None,
        pixelSizeX = None,
        pixelSizeY = None,
        width = None,
        height = None,
        tileSizeX = None,
        tileSizeY = None,
        orthorectify: bool = None,
        elevationModelName = None,
        noDataValue = None,
        includeTiePointGrids: bool = None,
        addDeltaBands: bool = None
        ):
        '''
        Reprojection of a source product to a target Coordinate Reference System.

        Parameters
        ----------
        wktFile : java.io.File
            A file which contains the target Coordinate Reference System in WKT format.
        crs : java.lang.String
            A text specifying the target Coordinate Reference System, either in WKT or as an authority code. For appropriate EPSG authority codes see (www.epsg-registry.org). AUTO authority can be used with code 42001 (UTM), and 42002 (Transverse Mercator) where the scene center is used as reference. Examples: EPSG:4326, AUTO:42001
        resamplingName : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for resampling of floating-point raster data.
            Default 'Nearest'
        referencePixelX : java.lang.Double
            The X-position of the reference pixel.
        referencePixelY : java.lang.Double
            The Y-position of the reference pixel.
        easting : java.lang.Double
            The easting of the reference pixel.
        northing : java.lang.Double
            The northing of the reference pixel.
        orientation : java.lang.Double
            The orientation of the output product (in degree).
            Default '0'
        pixelSizeX : java.lang.Double
            The pixel size in X direction given in CRS units.
        pixelSizeY : java.lang.Double
            The pixel size in Y direction given in CRS units.
        width : java.lang.Integer
            The width of the target product.
        height : java.lang.Integer
            The height of the target product.
        tileSizeX : java.lang.Integer
            The tile size in X direction.
        tileSizeY : java.lang.Integer
            The tile size in Y direction.
        orthorectify : boolean
            Whether the source product should be orthorectified. (Not applicable to all products)
            Default 'false'
        elevationModelName : java.lang.String
            The name of the elevation model for the orthorectification. If not given tie-point data is used.
        noDataValue : java.lang.Double
            The value used to indicate no-data.
        includeTiePointGrids : boolean
            Whether tie-point grids should be included in the output product.
            Default 'true'
        addDeltaBands : boolean
            Whether to add delta longitude and latitude bands.
            Default 'false'
        '''

        node = Node('Reproject')

        if wktFile:
            node.put('wktFile', wktFile)
        if crs:
            node.put('crs', crs)
        if resamplingName:
            node.put('resamplingName', resamplingName)
        if referencePixelX:
            node.put('referencePixelX', referencePixelX)
        if referencePixelY:
            node.put('referencePixelY', referencePixelY)
        if easting:
            node.put('easting', easting)
        if northing:
            node.put('northing', northing)
        if orientation:
            node.put('orientation', orientation)
        if pixelSizeX:
            node.put('pixelSizeX', pixelSizeX)
        if pixelSizeY:
            node.put('pixelSizeY', pixelSizeY)
        if width:
            node.put('width', width)
        if height:
            node.put('height', height)
        if tileSizeX:
            node.put('tileSizeX', tileSizeX)
        if tileSizeY:
            node.put('tileSizeY', tileSizeY)
        if orthorectify:
            node.put('orthorectify', orthorectify)
        if elevationModelName:
            node.put('elevationModelName', elevationModelName)
        if noDataValue:
            node.put('noDataValue', noDataValue)
        if includeTiePointGrids:
            node.put('includeTiePointGrids', includeTiePointGrids)
        if addDeltaBands:
            node.put('addDeltaBands', addDeltaBands)

        self.nodes.append(node)

    def add_olci_sensor_harmonisation(self,
        performSensorCrossCalibration: bool = None,
        copyInputBands: bool = None
        ):
        '''
        Performs sensor harmonisation on OLCI L1b product. Implements algorithm described in 'OLCI A/B Tandem Phase Analysis'

        Parameters
        ----------
        performSensorCrossCalibration : boolean
            If set to true, in addition to the camera homogenisation, sensor cross-calibration (i.e. S3A->S3B or S3B->S3A) is performed using linear regression
            Default 'false'
        copyInputBands : boolean
            If set to true, all bands of the input product (except for the radiances) are copied to the target product. If set to false, only the tie-point rasters are copied
            Default 'false'
        '''

        node = Node('OlciSensorHarmonisation')

        if performSensorCrossCalibration:
            node.put('performSensorCrossCalibration', performSensorCrossCalibration)
        if copyInputBands:
            node.put('copyInputBands', copyInputBands)

        self.nodes.append(node)

    def add_knn_classifier(self,
        numNeighbours: int = None,
        numTrainSamples: int = None,
        savedClassifierName = None,
        doLoadClassifier = None,
        doClassValQuantization = None,
        minClassValue = None,
        classValStepSize = None,
        classLevels: int = None,
        trainOnRaster = None,
        trainingBands = None,
        trainingVectors = None,
        featureBands = None,
        labelSource = None,
        evaluateClassifier = None,
        evaluateFeaturePowerSet = None,
        minPowerSetSize = None,
        maxPowerSetSize = None
        ):
        '''
        K-Nearest Neighbour classifier

        Parameters
        ----------
        numNeighbours : int
            The number of neighbours
            Default '5'
        numTrainSamples : int
            The number of training samples
            Default '5000'
        savedClassifierName : java.lang.String
            The saved classifier name
        doLoadClassifier : java.lang.Boolean
            Choose to save or load classifier
            Default 'false'
        doClassValQuantization : java.lang.Boolean
            Quantization for raster traiing
            Default 'true'
        minClassValue : java.lang.Double
            Quantization min class value for raster traiing
            Default '0.0'
        classValStepSize : java.lang.Double
            Quantization step size for raster traiing
            Default '5.0'
        classLevels : int
            Quantization class levels for raster traiing
            Default '101'
        trainOnRaster : java.lang.Boolean
            Train on raster or vector data
            Default 'true'
        trainingBands : java.lang.String[]
            Raster bands to train on
        trainingVectors : java.lang.String[]
            Vectors to train on
        featureBands : java.lang.String[]
            Names of bands to be used as features
        labelSource : java.lang.String
            'VectorNodeName' or specific Attribute name
        evaluateClassifier : java.lang.Boolean
            Evaluate classifier and features
        evaluateFeaturePowerSet : java.lang.Boolean
            Evaluate the power set of features
            Default 'false'
        minPowerSetSize : java.lang.Integer
            Minimum size of the power set of features
            Default '2'
        maxPowerSetSize : java.lang.Integer
            Maximum size of the power set of features
            Default '7'
        '''

        node = Node('KNN-Classifier')

        if numNeighbours:
            node.put('numNeighbours', numNeighbours)
        if numTrainSamples:
            node.put('numTrainSamples', numTrainSamples)
        if savedClassifierName:
            node.put('savedClassifierName', savedClassifierName)
        if doLoadClassifier:
            node.put('doLoadClassifier', doLoadClassifier)
        if doClassValQuantization:
            node.put('doClassValQuantization', doClassValQuantization)
        if minClassValue:
            node.put('minClassValue', minClassValue)
        if classValStepSize:
            node.put('classValStepSize', classValStepSize)
        if classLevels:
            node.put('classLevels', classLevels)
        if trainOnRaster:
            node.put('trainOnRaster', trainOnRaster)
        if trainingBands:
            node.put('trainingBands', trainingBands)
        if trainingVectors:
            node.put('trainingVectors', trainingVectors)
        if featureBands:
            node.put('featureBands', featureBands)
        if labelSource:
            node.put('labelSource', labelSource)
        if evaluateClassifier:
            node.put('evaluateClassifier', evaluateClassifier)
        if evaluateFeaturePowerSet:
            node.put('evaluateFeaturePowerSet', evaluateFeaturePowerSet)
        if minPowerSetSize:
            node.put('minPowerSetSize', minPowerSetSize)
        if maxPowerSetSize:
            node.put('maxPowerSetSize', maxPowerSetSize)

        self.nodes.append(node)

    def add_meris_correct_radiometry(self,
        doCalibration: bool = None,
        sourceRacFile = None,
        targetRacFile = None,
        doSmile: bool = None,
        doEqualization: bool = None,
        reproVersion = None,
        doRadToRefl: bool = None
        ):
        '''
        Performs radiometric corrections on MERIS L1b data products.

        Parameters
        ----------
        doCalibration : boolean
            Whether to perform the calibration.
            Default 'true'
        sourceRacFile : java.io.File
            The radiometric correction auxiliary file for the source product. The default 'MER_RAC_AXVIEC20050708_135553_20021224_121445_20041213_220000'
        targetRacFile : java.io.File
            The radiometric correction auxiliary file for the target product. The default 'MER_RAC_AXVACR20091016_154511_20021224_121445_20041213_220000'
        doSmile : boolean
            Whether to perform Smile-effect correction.
            Default 'true'
        doEqualization : boolean
            Perform removal of detector-to-detector systematic radiometric differences in MERIS L1b data products.
            Default 'true'
        reproVersion : org.esa.s3tbx.meris.radiometry.equalization.ReprocessingVersion, ['AUTO_DETECT', 'REPROCESSING_2', 'REPROCESSING_3']
            The version of the reprocessing the product comes from. Is only used if equalisation is enabled.
            Default 'AUTO_DETECT'
        doRadToRefl : boolean
            Whether to perform radiance-to-reflectance conversion. When selecting ENVISAT as target format, the radiance to reflectance conversion can not be performed.
            Default 'false'
        '''

        node = Node('Meris.CorrectRadiometry')

        if doCalibration:
            node.put('doCalibration', doCalibration)
        if sourceRacFile:
            node.put('sourceRacFile', sourceRacFile)
        if targetRacFile:
            node.put('targetRacFile', targetRacFile)
        if doSmile:
            node.put('doSmile', doSmile)
        if doEqualization:
            node.put('doEqualization', doEqualization)
        if reproVersion:
            node.put('reproVersion', reproVersion)
        if doRadToRefl:
            node.put('doRadToRefl', doRadToRefl)

        self.nodes.append(node)

    def add_statistics_op(self,
        sourceProductPaths = None,
        shapefile = None,
        featureId = None,
        startDate = None,
        endDate = None,
        bandConfigurations = None,
        outputShapefile = None,
        outputAsciiFile = None,
        percentiles = None,
        accuracy: int = None,
        interval = None,
        writeDataTypesSeparately: bool = None
        ):
        '''
        Computes statistics for an arbitrary number of source products.

        Parameters
        ----------
        sourceProductPaths : java.lang.String[]
            A comma-separated list of file paths specifying the source products.
            Each path may contain the wildcards '**' (matches recursively any directory),
            '*' (matches any character sequence in path names) and
            '?' (matches any single character).
            If, for example, all NetCDF files under /eodata/ shall be considered, use '/eodata/**/*.nc'.
        shapefile : java.io.File
            An ESRI shapefile, providing the considered geographical region(s) given as polygons. If null, all pixels are considered.
        featureId : java.lang.String
            The name of the attribute in the ESRI shapefile that shall be used to identify featuresin the output. If none is given or if the shapefile does not have the attribute, the feature id will beused. This parameter is case-sensitive. It is only considered when the shapefile parameter is set.
            Default 'name'
        startDate : org.esa.snap.core.datamodel.ProductData$UTC
            The start date. If not given, taken from the 'oldest' source product. Products that have a start date before the start date given by this parameter are not considered.
        endDate : org.esa.snap.core.datamodel.ProductData$UTC
            The end date. If not given, taken from the 'youngest' source product. Products that have an end date after the end date given by this parameter are not considered.
        bandConfigurations : org.esa.snap.statistics.BandConfiguration[]
            The band configurations. These configurations determine the input of the operator.
        outputShapefile : java.io.File
            The target file for shapefile output. Shapefile output will only be written if this parameter is set. The band mapping file will have the suffix _band_mapping.txt.
        outputAsciiFile : java.io.File
            The target file for ASCII output.The metadata file will have the suffix _metadata.txt.
            ASCII output will only be written if this parameter is set.
        percentiles : int[]
            The percentile levels that shall be created. Must be in the interval [0..100]
            Default '90,95'
        accuracy : int
            The degree of accuracy used for statistics computation. Higher numbers indicate higher accuracy but may lead to a considerably longer computation time.
            Default '3'
        interval : org.esa.snap.statistics.TimeIntervalDefinition
            If set, the StatisticsOp will divide the time between start and end time into time intervalsdefined by this parameter. All measures will be aggregated from products within these intervals. This parameter will only have an effect if the parameters start date and end date are set.
        writeDataTypesSeparately : boolean
            If true, categorical measures and quantitative measures will be written separately.
            Default 'false'
        '''

        node = Node('StatisticsOp')

        if sourceProductPaths:
            node.put('sourceProductPaths', sourceProductPaths)
        if shapefile:
            node.put('shapefile', shapefile)
        if featureId:
            node.put('featureId', featureId)
        if startDate:
            node.put('startDate', startDate)
        if endDate:
            node.put('endDate', endDate)
        if bandConfigurations:
            node.put('bandConfigurations', bandConfigurations)
        if outputShapefile:
            node.put('outputShapefile', outputShapefile)
        if outputAsciiFile:
            node.put('outputAsciiFile', outputAsciiFile)
        if percentiles:
            node.put('percentiles', percentiles)
        if accuracy:
            node.put('accuracy', accuracy)
        if interval:
            node.put('interval', interval)
        if writeDataTypesSeparately:
            node.put('writeDataTypesSeparately', writeDataTypesSeparately)

        self.nodes.append(node)

    def add_flip(self,
        sourceBandNames = None,
        flipType = None
        ):
        '''
        flips a product horizontal/vertical

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        flipType : java.lang.String, ['Horizontal', 'Vertical', 'Horizontal and Vertical']
            Default 'Vertical'
        '''

        node = Node('Flip')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if flipType:
            node.put('flipType', flipType)

        self.nodes.append(node)

    def add_meris_adapt_4_to3(self
        ):
        '''
        Provides the adaptation of MERIS L1b products from 4th to 3rd reprocessing.

        Parameters
        ----------
        '''

        node = Node('Meris.Adapt.4To3')


        self.nodes.append(node)

    def add_terrain_flattening(self,
        sourceBandNames = None,
        demName = None,
        demResamplingMethod = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        externalDEMApplyEGM = None,
        outputSimulatedImage = None,
        outputSigma0 = None,
        nodataValueAtSea: bool = None,
        additionalOverlap = None,
        oversamplingMultiple = None
        ):
        '''
        Terrain Flattening

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 1Sec HGT'
        demResamplingMethod : java.lang.String
            Default 'BILINEAR_INTERPOLATION'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        externalDEMApplyEGM : java.lang.Boolean
            Default 'false'
        outputSimulatedImage : java.lang.Boolean
            Default 'false'
        outputSigma0 : java.lang.Boolean
            Default 'false'
        nodataValueAtSea : boolean
            Mask the sea with no data value (faster)
            Default 'true'
        additionalOverlap : java.lang.Double
            The additional overlap percentage
            Default '0.1'
        oversamplingMultiple : java.lang.Double
            The oversampling factor
            Default '1.0'
        '''

        node = Node('Terrain-Flattening')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if demName:
            node.put('demName', demName)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if externalDEMApplyEGM:
            node.put('externalDEMApplyEGM', externalDEMApplyEGM)
        if outputSimulatedImage:
            node.put('outputSimulatedImage', outputSimulatedImage)
        if outputSigma0:
            node.put('outputSigma0', outputSigma0)
        if nodataValueAtSea:
            node.put('nodataValueAtSea', nodataValueAtSea)
        if additionalOverlap:
            node.put('additionalOverlap', additionalOverlap)
        if oversamplingMultiple:
            node.put('oversamplingMultiple', oversamplingMultiple)

        self.nodes.append(node)

    def add_ndi45_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redB4Factor: float = None,
        redB5Factor: float = None,
        redSourceBand4 = None,
        redSourceBand5 = None
        ):
        '''
        Normalized Difference Index using bands 4 and 5

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redB4Factor : float
            The value of the red source band (B4) is multiplied by this value.
            Default '1.0F'
        redB5Factor : float
            The value of the red source band (B5) is multiplied by this value.
            Default '1.0F'
        redSourceBand4 : java.lang.String
            The red band (B4) for the NDI45 computation. If not provided, the operator will try to find the best fitting band.
        redSourceBand5 : java.lang.String
            The red band (B5) for the NDI45 computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('Ndi45Op')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redB4Factor:
            node.put('redB4Factor', redB4Factor)
        if redB5Factor:
            node.put('redB5Factor', redB5Factor)
        if redSourceBand4:
            node.put('redSourceBand4', redSourceBand4)
        if redSourceBand5:
            node.put('redSourceBand5', redSourceBand5)

        self.nodes.append(node)

    def add_supervised_wishart_classification(self,
        trainingDataSet = None,
        windowSize: int = None
        ):
        '''
        Perform supervised Wishart classification

        Parameters
        ----------
        trainingDataSet : java.io.File
            The training data set file
        windowSize : int
            The sliding window size
            Default '5'
        '''

        node = Node('Supervised-Wishart-Classification')

        if trainingDataSet:
            node.put('trainingDataSet', trainingDataSet)
        if windowSize:
            node.put('windowSize', windowSize)

        self.nodes.append(node)

    def add_random_forest_classifier(self,
        treeCount: int = None,
        numTrainSamples: int = None,
        savedClassifierName = None,
        doLoadClassifier = None,
        doClassValQuantization = None,
        minClassValue = None,
        classValStepSize = None,
        classLevels: int = None,
        trainOnRaster = None,
        trainingBands = None,
        trainingVectors = None,
        featureBands = None,
        labelSource = None,
        evaluateClassifier = None,
        evaluateFeaturePowerSet = None,
        minPowerSetSize = None,
        maxPowerSetSize = None
        ):
        '''
        Random Forest based classifier

        Parameters
        ----------
        treeCount : int
            The number of trees
            Default '10'
        numTrainSamples : int
            The number of training samples
            Default '50000'
        savedClassifierName : java.lang.String
            The saved classifier name
        doLoadClassifier : java.lang.Boolean
            Choose to save or load classifier
            Default 'false'
        doClassValQuantization : java.lang.Boolean
            Quantization for raster traiing
            Default 'true'
        minClassValue : java.lang.Double
            Quantization min class value for raster traiing
            Default '0.0'
        classValStepSize : java.lang.Double
            Quantization step size for raster traiing
            Default '5.0'
        classLevels : int
            Quantization class levels for raster traiing
            Default '101'
        trainOnRaster : java.lang.Boolean
            Train on raster or vector data
            Default 'false'
        trainingBands : java.lang.String[]
            Raster bands to train on
        trainingVectors : java.lang.String[]
            Vectors to train on
        featureBands : java.lang.String[]
            Names of bands to be used as features
        labelSource : java.lang.String
            'VectorNodeName' or specific Attribute name
        evaluateClassifier : java.lang.Boolean
            Evaluate classifier and features
            Default 'false'
        evaluateFeaturePowerSet : java.lang.Boolean
            Evaluate the power set of features
            Default 'false'
        minPowerSetSize : java.lang.Integer
            Minimum size of the power set of features
            Default '2'
        maxPowerSetSize : java.lang.Integer
            Maximum size of the power set of features
            Default '7'
        '''

        node = Node('Random-Forest-Classifier')

        if treeCount:
            node.put('treeCount', treeCount)
        if numTrainSamples:
            node.put('numTrainSamples', numTrainSamples)
        if savedClassifierName:
            node.put('savedClassifierName', savedClassifierName)
        if doLoadClassifier:
            node.put('doLoadClassifier', doLoadClassifier)
        if doClassValQuantization:
            node.put('doClassValQuantization', doClassValQuantization)
        if minClassValue:
            node.put('minClassValue', minClassValue)
        if classValStepSize:
            node.put('classValStepSize', classValStepSize)
        if classLevels:
            node.put('classLevels', classLevels)
        if trainOnRaster:
            node.put('trainOnRaster', trainOnRaster)
        if trainingBands:
            node.put('trainingBands', trainingBands)
        if trainingVectors:
            node.put('trainingVectors', trainingVectors)
        if featureBands:
            node.put('featureBands', featureBands)
        if labelSource:
            node.put('labelSource', labelSource)
        if evaluateClassifier:
            node.put('evaluateClassifier', evaluateClassifier)
        if evaluateFeaturePowerSet:
            node.put('evaluateFeaturePowerSet', evaluateFeaturePowerSet)
        if minPowerSetSize:
            node.put('minPowerSetSize', minPowerSetSize)
        if maxPowerSetSize:
            node.put('maxPowerSetSize', maxPowerSetSize)

        self.nodes.append(node)

    def add_aatsr_sst(self,
        dual: bool = None,
        dualCoefficientsFile = None,
        dualMaskExpression = None,
        nadir: bool = None,
        nadirCoefficientsFile = None,
        nadirMaskExpression = None,
        invalidSstValue: float = None
        ):
        '''
        Computes sea surface temperature (SST) from (A)ATSR products.

        Parameters
        ----------
        dual : boolean
            Enables/disables generation of the dual-view SST
            Default 'true'
        dualCoefficientsFile : org.esa.s3tbx.aatsr.sst.AatsrSstOp$Files, ['AVERAGE_POLAR_DUAL_VIEW', 'AVERAGE_TEMPERATE_DUAL_VIEW', 'AVERAGE_TROPICAL_DUAL_VIEW', 'GRIDDED_POLAR_DUAL_VIEW', 'GRIDDED_TEMPERATE_DUAL_VIEW', 'GRIDDED_TROPICAL_DUAL_VIEW', 'GRIDDED_DUAL_VIEW_IPF']
            Coefficient file for the dual-view SST
            Default 'AVERAGE_POLAR_DUAL_VIEW'
        dualMaskExpression : java.lang.String
            ROI-mask used for the dual-view SST
            Default '!cloud_flags_nadir.LAND and !cloud_flags_nadir.CLOUDY and !cloud_flags_nadir.SUN_GLINT and !cloud_flags_fward.LAND and !cloud_flags_fward.CLOUDY and !cloud_flags_fward.SUN_GLINT'
        nadir : boolean
            Enables/disables generation of the nadir-view SST
            Default 'true'
        nadirCoefficientsFile : org.esa.s3tbx.aatsr.sst.AatsrSstOp$Files, ['AVERAGE_POLAR_SINGLE_VIEW', 'AVERAGE_TEMPERATE_SINGLE_VIEW', 'AVERAGE_TROPICAL_SINGLE_VIEW', 'GRIDDED_POLAR_SINGLE_VIEW', 'GRIDDED_TEMPERATE_SINGLE_VIEW', 'GRIDDED_TROPICAL_SINGLE_VIEW']
            Coefficient file for the nadir-view SST
            Default 'AVERAGE_POLAR_SINGLE_VIEW'
        nadirMaskExpression : java.lang.String
            ROI-mask used for the nadir-view SST
            Default '!cloud_flags_nadir.LAND and !cloud_flags_nadir.CLOUDY and !cloud_flags_nadir.SUN_GLINT'
        invalidSstValue : float
            Value used to fill invalid SST pixels
            Default '-999.0f'
        '''

        node = Node('Aatsr.SST')

        if dual:
            node.put('dual', dual)
        if dualCoefficientsFile:
            node.put('dualCoefficientsFile', dualCoefficientsFile)
        if dualMaskExpression:
            node.put('dualMaskExpression', dualMaskExpression)
        if nadir:
            node.put('nadir', nadir)
        if nadirCoefficientsFile:
            node.put('nadirCoefficientsFile', nadirCoefficientsFile)
        if nadirMaskExpression:
            node.put('nadirMaskExpression', nadirMaskExpression)
        if invalidSstValue:
            node.put('invalidSstValue', invalidSstValue)

        self.nodes.append(node)

    def add_aatsr_ungrid(self,
        L1BCharacterisationFile = None,
        cornerReferenceFlag: bool = None,
        topographicFlag: bool = None,
        topographyHomogenity: float = None
        ):
        '''
        Ungrids (A)ATSR L1B products and extracts geolocation and pixel field of view data.

        Parameters
        ----------
        L1BCharacterisationFile : java.io.File
            L1B characterisation file is needed to specify first forward pixel and first nadir pixel
        cornerReferenceFlag : boolean
            Choose the pixel coordinate reference point for use in the output file. 
            Check for Corner (default), un-check for Centre.
            Default 'true'
        topographicFlag : boolean
            Option to apply topographic corrections to tie points
            Default 'false'
        topographyHomogenity : double
            Distance (image coordinates) pixel can be from tie-point to have topo correction applied
            Default '0.05'
        '''

        node = Node('AATSR.Ungrid')

        if L1BCharacterisationFile:
            node.put('L1BCharacterisationFile', L1BCharacterisationFile)
        if cornerReferenceFlag:
            node.put('cornerReferenceFlag', cornerReferenceFlag)
        if topographicFlag:
            node.put('topographicFlag', topographicFlag)
        if topographyHomogenity:
            node.put('topographyHomogenity', topographyHomogenity)

        self.nodes.append(node)

    def add_reflectance_to_radiance_op(self,
        solarIrradiance: float = None,
        u: float = None,
        incidenceAngle: float = None,
        sourceBandNames = None,
        copyMasks: bool = None
        ):
        '''
        The 'Reflectance To Radiance Processor' operator retrieves the radiance from reflectance using Sentinel-2 products

        Parameters
        ----------
        solarIrradiance : float
            The solar irradiance.
        u : float
            U
        incidenceAngle : float
            The incidence angle in degrees.
        sourceBandNames : java.lang.String[]
            The source bands for the computation.
        copyMasks : boolean
            Copy masks from the source product
            Default 'false'
        '''

        node = Node('ReflectanceToRadianceOp')

        if solarIrradiance:
            node.put('solarIrradiance', solarIrradiance)
        if u:
            node.put('u', u)
        if incidenceAngle:
            node.put('incidenceAngle', incidenceAngle)
        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if copyMasks:
            node.put('copyMasks', copyMasks)

        self.nodes.append(node)

    def add_read(self,
        file = None,
        formatName = None,
        bandNames = None,
        maskNames = None,
        pixelRegion = None,
        geometryRegion = None,
        useAdvancedOptions: bool = None,
        copyMetadata: bool = None
        ):
        '''
        Reads a data product from a given file location.

        Parameters
        ----------
        file : java.io.File
            The file from which the data product is read.
        formatName : java.lang.String
            An (optional) format name.
        bandNames : java.lang.String[]
            The list of source bands.
        maskNames : java.lang.String[]
            The list of source masks.
        pixelRegion : java.awt.Rectangle
            The subset region in pixel coordinates.
            Use the following format: {x>,{y>,{width>,{height>
            If not given, the entire scene is used. The 'geoRegion' parameter has precedence over this parameter.
        geometryRegion : org.locationtech.jts.geom.Geometry
            The subset region in geographical coordinates using WKT-format,
            e.g. POLYGON(({lon1} {lat1}, {lon2} {lat2}, ..., {lon1} {lat1}))
            (make sure to quote the option due to spaces in {geometry}).
            If not given, the entire scene is used.
        useAdvancedOptions : boolean
            Whether to use advanced options for reading of the source product.
            Default 'false'
        copyMetadata : boolean
            Whether to copy the metadata of the source product.
            Default 'true'
        '''

        node = Node('Read')

        if file:
            node.put('file', file)
        if formatName:
            node.put('formatName', formatName)
        if bandNames:
            node.put('bandNames', bandNames)
        if maskNames:
            node.put('maskNames', maskNames)
        if pixelRegion:
            node.put('pixelRegion', pixelRegion)
        if geometryRegion:
            node.put('geometryRegion', geometryRegion)
        if useAdvancedOptions:
            node.put('useAdvancedOptions', useAdvancedOptions)
        if copyMetadata:
            node.put('copyMetadata', copyMetadata)

        self.nodes.append(node)

    def add_bands_difference_op(self
        ):
        '''
        None

        Parameters
        ----------
        '''

        node = Node('BandsDifferenceOp')


        self.nodes.append(node)

    def add_stack_split(self,
        targetFolder = None,
        formatName = None
        ):
        '''
        Writes all bands to files.

        Parameters
        ----------
        targetFolder : java.io.File
            The output folder to which the data product is written.
            Default 'target'
        formatName : java.lang.String
            The name of the output file format.
            Default 'BEAM-DIMAP'
        '''

        node = Node('Stack-Split')

        if targetFolder:
            node.put('targetFolder', targetFolder)
        if formatName:
            node.put('formatName', formatName)

        self.nodes.append(node)

    def add_pssra_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        Pigment Specific Simple Ratio, chlorophyll index

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the PSSRa computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the PSSRa computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('PssraOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_compute_slope_aspect(self,
        demName = None,
        demResamplingMethod = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        externalDEMApplyEGM = None,
        demBandName = None
        ):
        '''
        Compute Slope and Aspect from DEM

        Parameters
        ----------
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 1Sec HGT'
        demResamplingMethod : java.lang.String
            Default 'BILINEAR_INTERPOLATION'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        externalDEMApplyEGM : java.lang.Boolean
            Default 'false'
        demBandName : java.lang.String
            Default 'elevation'
        '''

        node = Node('Compute-Slope-Aspect')

        if demName:
            node.put('demName', demName)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if externalDEMApplyEGM:
            node.put('externalDEMApplyEGM', externalDEMApplyEGM)
        if demBandName:
            node.put('demBandName', demBandName)

        self.nodes.append(node)

    def add_phase_to_height(self,
        nPoints: int = None,
        nHeights: int = None,
        degree1D: int = None,
        degree2D: int = None,
        orbitDegree: int = None
        ):
        '''
        Phase to Height conversion

        Parameters
        ----------
        nPoints : int, ['100', '200', '300', '400', '500']
            Number of points for evaluation of flat earth phase at different altitudes
            Default '200'
        nHeights : int, ['2', '3', '4', '5']
            Number of height samples in range [0,5000)
            Default '3'
        degree1D : int, ['1', '2', '3', '4', '5']
            Degree of the 1D polynomial to fit reference phase through.
            Default '2'
        degree2D : int, ['1', '2', '3', '4', '5', '6', '7', '8']
            Degree of the 2D polynomial to fit reference phase through.
            Default '5'
        orbitDegree : int, ['2', '3', '4', '5']
            Degree of orbit (polynomial) interpolator
            Default '3'
        '''

        node = Node('PhaseToHeight')

        if nPoints:
            node.put('nPoints', nPoints)
        if nHeights:
            node.put('nHeights', nHeights)
        if degree1D:
            node.put('degree1D', degree1D)
        if degree2D:
            node.put('degree2D', degree2D)
        if orbitDegree:
            node.put('orbitDegree', orbitDegree)

        self.nodes.append(node)

    def add_gaseous_absorption(self
        ):
        '''
        Correct the influence of atmospheric gas absorption for those OLCI channels.

        Parameters
        ----------
        '''

        node = Node('GaseousAbsorption')


        self.nodes.append(node)

    def add_olci_o2a_harmonisation(self,
        alternativeAltitudeBandName = None,
        processOnlyBand13: bool = None,
        writeHarmonisedRadiances: bool = None
        ):
        '''
        Performs O2A band harmonisation on OLCI L1b product. Implements update v4 of R.Preusker, June 2020.

        Parameters
        ----------
        alternativeAltitudeBandName : java.lang.String
            Name of alternative altitude band in source product (i.e. introduced from an external DEM). Altitude is expected in meters.
        processOnlyBand13 : boolean
            If set to true, only band 13 needed for cloud detection will be processed, otherwise bands 13-15.
            Default 'true'
        writeHarmonisedRadiances : boolean
            If set to true, harmonised radiances of processed band(s) will be written to target product.
            Default 'true'
        '''

        node = Node('OlciO2aHarmonisation')

        if alternativeAltitudeBandName:
            node.put('alternativeAltitudeBandName', alternativeAltitudeBandName)
        if processOnlyBand13:
            node.put('processOnlyBand13', processOnlyBand13)
        if writeHarmonisedRadiances:
            node.put('writeHarmonisedRadiances', writeHarmonisedRadiances)

        self.nodes.append(node)

    def add_s2rep_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redB4Factor: float = None,
        redB5Factor: float = None,
        redB6Factor: float = None,
        nirFactor: float = None,
        redSourceBand4 = None,
        redSourceBand5 = None,
        redSourceBand6 = None,
        nirSourceBand = None
        ):
        '''
        Sentinel-2 red-edge position index

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redB4Factor : float
            The value of the red source band (B4) is multiplied by this value.
            Default '1.0F'
        redB5Factor : float
            The value of the red source band (B5) is multiplied by this value.
            Default '1.0F'
        redB6Factor : float
            The value of the red source band (B6) is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand4 : java.lang.String
            The red band (B4) for the S2REP computation. If not provided, the operator will try to find the best fitting band.
        redSourceBand5 : java.lang.String
            The red band (B5) for the S2REP computation. If not provided, the operator will try to find the best fitting band.
        redSourceBand6 : java.lang.String
            The red band (B6) for the S2REP computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the S2REP computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('S2repOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redB4Factor:
            node.put('redB4Factor', redB4Factor)
        if redB5Factor:
            node.put('redB5Factor', redB5Factor)
        if redB6Factor:
            node.put('redB6Factor', redB6Factor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand4:
            node.put('redSourceBand4', redSourceBand4)
        if redSourceBand5:
            node.put('redSourceBand5', redSourceBand5)
        if redSourceBand6:
            node.put('redSourceBand6', redSourceBand6)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_c_p_stokes_parameters(self,
        windowSizeXStr = None,
        windowSizeYStr = None,
        outputStokesVector: bool = None,
        outputDegreeOfPolarization: bool = None,
        outputDegreeOfDepolarization: bool = None,
        outputDegreeOfCircularity: bool = None,
        outputDegreeOfEllipticity: bool = None,
        outputCPR: bool = None,
        outputLPR: bool = None,
        outputRelativePhase: bool = None,
        outputAlphas: bool = None,
        outputConformity: bool = None,
        outputPhasePhi: bool = None
        ):
        '''
        Generates compact polarimetric Stokes child parameters

        Parameters
        ----------
        windowSizeXStr : java.lang.String, ['3', '5', '7', '9', '11', '13', '15', '17', '19']
            Default '5'
        windowSizeYStr : java.lang.String, ['3', '5', '7', '9', '11', '13', '15', '17', '19']
            Default '5'
        outputStokesVector : boolean
            Output Stokes vector
            Default 'false'
        outputDegreeOfPolarization : boolean
            Output degree of polarization
            Default 'true'
        outputDegreeOfDepolarization : boolean
            Output degree of depolarization
            Default 'true'
        outputDegreeOfCircularity : boolean
            Output degree of circularity
            Default 'true'
        outputDegreeOfEllipticity : boolean
            Output degree of ellipticity
            Default 'true'
        outputCPR : boolean
            Output circular polarization ratio
            Default 'true'
        outputLPR : boolean
            Output linear polarization ratio
            Default 'true'
        outputRelativePhase : boolean
            Output relative phase
            Default 'true'
        outputAlphas : boolean
            Output alphas
            Default 'true'
        outputConformity : boolean
            Output conformity coefficient
            Default 'true'
        outputPhasePhi : boolean
            Output phase phi
            Default 'true'
        '''

        node = Node('CP-Stokes-Parameters')

        if windowSizeXStr:
            node.put('windowSizeXStr', windowSizeXStr)
        if windowSizeYStr:
            node.put('windowSizeYStr', windowSizeYStr)
        if outputStokesVector:
            node.put('outputStokesVector', outputStokesVector)
        if outputDegreeOfPolarization:
            node.put('outputDegreeOfPolarization', outputDegreeOfPolarization)
        if outputDegreeOfDepolarization:
            node.put('outputDegreeOfDepolarization', outputDegreeOfDepolarization)
        if outputDegreeOfCircularity:
            node.put('outputDegreeOfCircularity', outputDegreeOfCircularity)
        if outputDegreeOfEllipticity:
            node.put('outputDegreeOfEllipticity', outputDegreeOfEllipticity)
        if outputCPR:
            node.put('outputCPR', outputCPR)
        if outputLPR:
            node.put('outputLPR', outputLPR)
        if outputRelativePhase:
            node.put('outputRelativePhase', outputRelativePhase)
        if outputAlphas:
            node.put('outputAlphas', outputAlphas)
        if outputConformity:
            node.put('outputConformity', outputConformity)
        if outputPhasePhi:
            node.put('outputPhasePhi', outputPhasePhi)

        self.nodes.append(node)

    def add_terrain_correction(self,
        sourceBandNames = None,
        demName = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        externalDEMApplyEGM = None,
        demResamplingMethod = None,
        imgResamplingMethod = None,
        pixelSpacingInMeter: float = None,
        pixelSpacingInDegree: float = None,
        mapProjection = None,
        alignToStandardGrid: bool = None,
        standardGridOriginX: float = None,
        standardGridOriginY: float = None,
        nodataValueAtSea: bool = None,
        saveDEM: bool = None,
        saveLatLon: bool = None,
        saveIncidenceAngleFromEllipsoid: bool = None,
        saveLocalIncidenceAngle: bool = None,
        saveProjectedLocalIncidenceAngle: bool = None,
        saveSelectedSourceBand: bool = None,
        saveLayoverShadowMask: bool = None,
        outputComplex: bool = None,
        applyRadiometricNormalization: bool = None,
        saveSigmaNought: bool = None,
        saveGammaNought: bool = None,
        saveBetaNought: bool = None,
        incidenceAngleForSigma0 = None,
        incidenceAngleForGamma0 = None,
        auxFile = None,
        externalAuxFile = None
        ):
        '''
        RD method for orthorectification

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        externalDEMApplyEGM : java.lang.Boolean
            Default 'true'
        demResamplingMethod : java.lang.String, ['NEAREST_NEIGHBOUR', 'BILINEAR_INTERPOLATION', 'CUBIC_CONVOLUTION', 'BISINC_5_POINT_INTERPOLATION', 'BISINC_11_POINT_INTERPOLATION', 'BISINC_21_POINT_INTERPOLATION', 'BICUBIC_INTERPOLATION', 'DELAUNAY_INTERPOLATION']
            Default 'BILINEAR_INTERPOLATION'
        imgResamplingMethod : java.lang.String, ['NEAREST_NEIGHBOUR', 'BILINEAR_INTERPOLATION', 'CUBIC_CONVOLUTION', 'BISINC_5_POINT_INTERPOLATION', 'BISINC_11_POINT_INTERPOLATION', 'BISINC_21_POINT_INTERPOLATION', 'BICUBIC_INTERPOLATION']
            Default 'BILINEAR_INTERPOLATION'
        pixelSpacingInMeter : double
            The pixel spacing in meters
            Default '0'
        pixelSpacingInDegree : double
            The pixel spacing in degrees
            Default '0'
        mapProjection : java.lang.String
            The coordinate reference system in well known text format
            Default 'WGS84(DD)'
        alignToStandardGrid : boolean
            Force the image grid to be aligned with a specific point
            Default 'false'
        standardGridOriginX : double
            x-coordinate of the standard grid's origin point
            Default '0'
        standardGridOriginY : double
            y-coordinate of the standard grid's origin point
            Default '0'
        nodataValueAtSea : boolean
            Mask the sea with no data value (faster)
            Default 'true'
        saveDEM : boolean
            Default 'false'
        saveLatLon : boolean
            Default 'false'
        saveIncidenceAngleFromEllipsoid : boolean
            Default 'false'
        saveLocalIncidenceAngle : boolean
            Default 'false'
        saveProjectedLocalIncidenceAngle : boolean
            Default 'false'
        saveSelectedSourceBand : boolean
            Default 'true'
        saveLayoverShadowMask : boolean
            Default 'false'
        outputComplex : boolean
            Default 'false'
        applyRadiometricNormalization : boolean
            Default 'false'
        saveSigmaNought : boolean
            Default 'false'
        saveGammaNought : boolean
            Default 'false'
        saveBetaNought : boolean
            Default 'false'
        incidenceAngleForSigma0 : java.lang.String, ['Use incidence angle from Ellipsoid', 'Use local incidence angle from DEM', 'Use projected local incidence angle from DEM']
            Default 'Use projected local incidence angle from DEM'
        incidenceAngleForGamma0 : java.lang.String, ['Use incidence angle from Ellipsoid', 'Use local incidence angle from DEM', 'Use projected local incidence angle from DEM']
            Default 'Use projected local incidence angle from DEM'
        auxFile : java.lang.String, ['Latest Auxiliary File', 'Product Auxiliary File', 'External Auxiliary File']
            The auxiliary file
            Default 'Latest Auxiliary File'
        externalAuxFile : java.io.File
            The antenne elevation pattern gain auxiliary data file.
        '''

        node = Node('Terrain-Correction')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if demName:
            node.put('demName', demName)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if externalDEMApplyEGM:
            node.put('externalDEMApplyEGM', externalDEMApplyEGM)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if imgResamplingMethod:
            node.put('imgResamplingMethod', imgResamplingMethod)
        if pixelSpacingInMeter:
            node.put('pixelSpacingInMeter', pixelSpacingInMeter)
        if pixelSpacingInDegree:
            node.put('pixelSpacingInDegree', pixelSpacingInDegree)
        if mapProjection:
            node.put('mapProjection', mapProjection)
        if alignToStandardGrid:
            node.put('alignToStandardGrid', alignToStandardGrid)
        if standardGridOriginX:
            node.put('standardGridOriginX', standardGridOriginX)
        if standardGridOriginY:
            node.put('standardGridOriginY', standardGridOriginY)
        if nodataValueAtSea:
            node.put('nodataValueAtSea', nodataValueAtSea)
        if saveDEM:
            node.put('saveDEM', saveDEM)
        if saveLatLon:
            node.put('saveLatLon', saveLatLon)
        if saveIncidenceAngleFromEllipsoid:
            node.put('saveIncidenceAngleFromEllipsoid', saveIncidenceAngleFromEllipsoid)
        if saveLocalIncidenceAngle:
            node.put('saveLocalIncidenceAngle', saveLocalIncidenceAngle)
        if saveProjectedLocalIncidenceAngle:
            node.put('saveProjectedLocalIncidenceAngle', saveProjectedLocalIncidenceAngle)
        if saveSelectedSourceBand:
            node.put('saveSelectedSourceBand', saveSelectedSourceBand)
        if saveLayoverShadowMask:
            node.put('saveLayoverShadowMask', saveLayoverShadowMask)
        if outputComplex:
            node.put('outputComplex', outputComplex)
        if applyRadiometricNormalization:
            node.put('applyRadiometricNormalization', applyRadiometricNormalization)
        if saveSigmaNought:
            node.put('saveSigmaNought', saveSigmaNought)
        if saveGammaNought:
            node.put('saveGammaNought', saveGammaNought)
        if saveBetaNought:
            node.put('saveBetaNought', saveBetaNought)
        if incidenceAngleForSigma0:
            node.put('incidenceAngleForSigma0', incidenceAngleForSigma0)
        if incidenceAngleForGamma0:
            node.put('incidenceAngleForGamma0', incidenceAngleForGamma0)
        if auxFile:
            node.put('auxFile', auxFile)
        if externalAuxFile:
            node.put('externalAuxFile', externalAuxFile)

        self.nodes.append(node)

    def add_binning(self,
        sourceProductPaths = None,
        sourceProductFormat = None,
        sourceGraphPaths = None,
        region = None,
        startDateTime = None,
        periodDuration = None,
        timeFilterMethod = None,
        minDataHour = None,
        numRows: int = None,
        superSampling = None,
        maxDistanceOnEarth = None,
        maskExpr = None,
        variableConfigs = None,
        aggregatorConfigs = None,
        postProcessorConfig = None,
        outputType = None,
        outputFile = None,
        outputFormat = None,
        bandConfigurations = None,
        productCustomizerConfig = None,
        outputBinnedData: bool = None,
        outputTargetProduct: bool = None,
        metadataPropertiesFile = None,
        metadataTemplateDir = None,
        metadataAggregatorName = None,
        planetaryGridClass = None
        ):
        '''
        Performs spatial and temporal aggregation of pixel values into cells ('bins') of a planetary grid

        Parameters
        ----------
        sourceProductPaths : java.lang.String[]
            A comma-separated list of file paths specifying the source products.
            Each path may contain the wildcards '**' (matches recursively any directory),
            '*' (matches any character sequence in path names) and
            '?' (matches any single character).
        sourceProductFormat : java.lang.String
            The common product format of all source products.
            This parameter is optional and may be used in conjunction with
            parameter 'sourceProductPaths'. Can be set if multiple reader are 
            available for the source files and a specific one shall be used.Try "NetCDF-CF", "GeoTIFF", "BEAM-DIMAP", or "ENVISAT", etc.
        sourceGraphPaths : java.lang.String[]
            A comma-separated list of file paths specifying the source graphs.
            Each path may contain the wildcards '**' (matches recursively any directory),
            '*' (matches any character sequence in path names) and
            '?' (matches any single character).
        region : org.locationtech.jts.geom.Geometry
            The considered geographical region as a geometry in well-known text format (WKT).
            If not given, the geographical region will be computed according to the extents of the input products.
        startDateTime : java.lang.String
            The UTC start date of the binning period.
            The format is either 'yyyy-MM-dd HH:mm:ss' or 'yyyy-MM-dd'.
             If only the date part is given, the time 00:00:00 is assumed.
        periodDuration : java.lang.Double
            Duration of the binning period in days.
        timeFilterMethod : org.esa.snap.binning.operator.BinningOp$TimeFilterMethod
            The method that is used to decide which source pixels are used with respect to their observation time.
            'NONE': ignore pixel observation time, use all source pixels.
            'TIME_RANGE': use all pixels that have been acquired in the given binning period.
            'SPATIOTEMPORAL_DATA_DAY': use a sensor-dependent, spatial "data-day" definition with the goal
            to minimise the time between the first and last observation contributing to the same bin in the given binning period.
            The decision, whether a source pixel contributes to a bin or not, is a function of the pixel's observation longitude and time.
            Requires the parameter 'minDataHour'.
            Default 'NONE'
        minDataHour : java.lang.Double
            A sensor-dependent constant given in hours of a day (0 to 24)
            at which a sensor has a minimum number of observations at the date line (the 180 degree meridian).
            Only used if parameter 'dataDayMode' is set to 'SPATIOTEMPORAL_DATADAY'. This is usually the equator crossing time (ECT)
        numRows : int
            Number of rows in the (global) planetary grid. Must be even.
            Default '2160'
        superSampling : java.lang.Integer
            The square of the number of pixels used for super-sampling an input pixel into multiple sub-pixels
            Default '1'
        maxDistanceOnEarth : java.lang.Integer
            Skips binning of sub-pixel if distance on earth to the center of the main-pixel is larger as this value. A value <=0 disables this check
            Default '-1'
        maskExpr : java.lang.String
            The band maths expression used to filter input pixels
        variableConfigs : org.esa.snap.binning.operator.VariableConfig[]
            List of variables. A variable will generate a virtual band
            in each source data product, so that it can be used as input for the binning.
        aggregatorConfigs : org.esa.snap.binning.AggregatorConfig[]
            List of aggregators. Aggregators generate the bands in the binned output products
        postProcessorConfig : org.esa.snap.binning.CellProcessorConfig
        outputType : java.lang.String, ['Product', 'RGB', 'Grey']
            Default 'Product'
        outputFile : java.lang.String
        outputFormat : java.lang.String
            Default 'BEAM-DIMAP'
        bandConfigurations : org.esa.snap.binning.operator.BinningOp$BandConfiguration[]
            Configures the target bands. Not needed if output type 'Product' is chosen.
        productCustomizerConfig : org.esa.snap.binning.ProductCustomizerConfig
        outputBinnedData : boolean
            If true, a SeaDAS-style, binned data NetCDF file is written in addition to the
            target product. The output file name will be {target}-bins.nc
            Default 'false'
        outputTargetProduct : boolean
            If true, a mapped product is written. Set this to 'false' if only a binned product is needed.
            Default 'true'
        metadataPropertiesFile : java.io.File
            The name of the file containing metadata key-value pairs (google "Java Properties file format").
            Default './metadata.properties'
        metadataTemplateDir : java.io.File
            The name of the directory containing metadata templates (google "Apache Velocity VTL format").
            Default '.'
        metadataAggregatorName : java.lang.String
            The type of metadata aggregation to be used. Possible values are:
            'NAME': aggregate the name of each input product
            'FIRST_HISTORY': aggregates all input product names and the processing history of the first product
            'ALL_HISTORIES': aggregates all input product names and processing histories
            Default 'NAME'
        planetaryGridClass : java.lang.String
            Default 'org.esa.snap.binning.support.SEAGrid'
        '''

        node = Node('Binning')

        if sourceProductPaths:
            node.put('sourceProductPaths', sourceProductPaths)
        if sourceProductFormat:
            node.put('sourceProductFormat', sourceProductFormat)
        if sourceGraphPaths:
            node.put('sourceGraphPaths', sourceGraphPaths)
        if region:
            node.put('region', region)
        if startDateTime:
            node.put('startDateTime', startDateTime)
        if periodDuration:
            node.put('periodDuration', periodDuration)
        if timeFilterMethod:
            node.put('timeFilterMethod', timeFilterMethod)
        if minDataHour:
            node.put('minDataHour', minDataHour)
        if numRows:
            node.put('numRows', numRows)
        if superSampling:
            node.put('superSampling', superSampling)
        if maxDistanceOnEarth:
            node.put('maxDistanceOnEarth', maxDistanceOnEarth)
        if maskExpr:
            node.put('maskExpr', maskExpr)
        if variableConfigs:
            node.put('variableConfigs', variableConfigs)
        if aggregatorConfigs:
            node.put('aggregatorConfigs', aggregatorConfigs)
        if postProcessorConfig:
            node.put('postProcessorConfig', postProcessorConfig)
        if outputType:
            node.put('outputType', outputType)
        if outputFile:
            node.put('outputFile', outputFile)
        if outputFormat:
            node.put('outputFormat', outputFormat)
        if bandConfigurations:
            node.put('bandConfigurations', bandConfigurations)
        if productCustomizerConfig:
            node.put('productCustomizerConfig', productCustomizerConfig)
        if outputBinnedData:
            node.put('outputBinnedData', outputBinnedData)
        if outputTargetProduct:
            node.put('outputTargetProduct', outputTargetProduct)
        if metadataPropertiesFile:
            node.put('metadataPropertiesFile', metadataPropertiesFile)
        if metadataTemplateDir:
            node.put('metadataTemplateDir', metadataTemplateDir)
        if metadataAggregatorName:
            node.put('metadataAggregatorName', metadataAggregatorName)
        if planetaryGridClass:
            node.put('planetaryGridClass', planetaryGridClass)

        self.nodes.append(node)

    def add_wind_field_estimation(self,
        sourceBandNames = None,
        windowSizeInKm: float = None
        ):
        '''
        Estimate wind speed and direction

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        windowSizeInKm : double
            Window size
            Default '20.0'
        '''

        node = Node('Wind-Field-Estimation')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if windowSizeInKm:
            node.put('windowSizeInKm', windowSizeInKm)

        self.nodes.append(node)

    def addc2rcc_viirs(self,
        validPixelExpression = None,
        salinity: float = None,
        temperature: float = None,
        ozone: float = None,
        press: float = None,
        atmosphericAuxDataPath = None,
        outputRtosa: bool = None,
        outputAsRrs: bool = None
        ):
        '''
        Performs atmospheric correction and IOP retrieval on Viirs L1C data products.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Defines the pixels which are valid for processing
            Default '!(l2_flags.LAND || rhot_862 > 0.25)'
        salinity : double
            The value used as salinity for the scene
            Default '35.0'
        temperature : double
            The value used as temperature for the scene
            Default '15.0'
        ozone : double
            The value used as ozone if not provided by auxiliary data
            Default '330'
        press : double
            The surface air pressure at sea level if not provided by auxiliary data
            Default '1000'
        atmosphericAuxDataPath : java.lang.String
            Path to the atmospheric auxiliary data directory. Use either this or tomsomiStartProduct, tomsomiEndProduct, ncepStartProduct and ncepEndProduct to use ozone and air pressure aux data for calculations. If the auxiliary data needed for interpolation not available in this path, the data will automatically downloaded.
        outputRtosa : boolean
            Default 'false'
        outputAsRrs : boolean
            Reflectance values in the target product shall be either written as remote sensing or water leaving reflectances
            Default 'false'
        '''

        node = Node('c2rcc.viirs')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if salinity:
            node.put('salinity', salinity)
        if temperature:
            node.put('temperature', temperature)
        if ozone:
            node.put('ozone', ozone)
        if press:
            node.put('press', press)
        if atmosphericAuxDataPath:
            node.put('atmosphericAuxDataPath', atmosphericAuxDataPath)
        if outputRtosa:
            node.put('outputRtosa', outputRtosa)
        if outputAsRrs:
            node.put('outputAsRrs', outputAsRrs)

        self.nodes.append(node)

    def add_polarimetric_classification(self,
        classification = None,
        windowSize: int = None,
        maxIterations: int = None,
        numInitialClasses: int = None,
        numFinalClasses: int = None,
        mixedCategoryThreshold: float = None,
        decomposition = None
        ):
        '''
        Perform Polarimetric classification of a given product

        Parameters
        ----------
        classification : java.lang.String, ['Cloude-Pottier', 'Cloude-Pottier Dual Pol', 'H Alpha Wishart', 'H Alpha Wishart Dual Pol', 'Freeman-Durden Wishart', 'General Wishart']
            Default 'H Alpha Wishart'
        windowSize : int
            The sliding window size
            Default '5'
        maxIterations : int
            The maximum number of iterations
            Default '3'
        numInitialClasses : int
            The initial number of classes
            Default '90'
        numFinalClasses : int
            The desired number of classes
            Default '15'
        mixedCategoryThreshold : double
            The threshold for classifying pixels to mixed category
            Default '0.5'
        decomposition : java.lang.String, ['Sinclair Decomposition', 'Pauli Decomposition', 'Freeman-Durden Decomposition', 'Generalized Freeman-Durden Decomposition', 'Yamaguchi Decomposition', 'van Zyl Decomposition', 'H-A-Alpha Quad Pol Decomposition', 'Cloude Decomposition', 'Touzi Decomposition']
            Default 'Sinclair Decomposition'
        '''

        node = Node('Polarimetric-Classification')

        if classification:
            node.put('classification', classification)
        if windowSize:
            node.put('windowSize', windowSize)
        if maxIterations:
            node.put('maxIterations', maxIterations)
        if numInitialClasses:
            node.put('numInitialClasses', numInitialClasses)
        if numFinalClasses:
            node.put('numFinalClasses', numFinalClasses)
        if mixedCategoryThreshold:
            node.put('mixedCategoryThreshold', mixedCategoryThreshold)
        if decomposition:
            node.put('decomposition', decomposition)

        self.nodes.append(node)

    def add_fill_band(self,
        copyAllTiePoints: bool = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        '''

        node = Node('FillBand')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)

        self.nodes.append(node)

    def add_principle_components(self,
        sourceBandNames = None,
        selectEigenvaluesBy = None,
        eigenvalueThreshold: float = None,
        numPCA: int = None,
        showEigenvalues = None,
        subtractMeanImage = None
        ):
        '''
        Principle Component Analysis

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        selectEigenvaluesBy : java.lang.String, ['Eigenvalue Threshold', 'Number of Eigenvalues']
            Default 'Eigenvalue Threshold'
        eigenvalueThreshold : double
            The threshold for selecting eigenvalues
            Default '100'
        numPCA : int
            The number of PCA images output
            Default '1'
        showEigenvalues : java.lang.Boolean
            Show the eigenvalues
            Default '1'
        subtractMeanImage : java.lang.Boolean
            Subtract mean image
            Default '1'
        '''

        node = Node('Principle-Components')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if selectEigenvaluesBy:
            node.put('selectEigenvaluesBy', selectEigenvaluesBy)
        if eigenvalueThreshold:
            node.put('eigenvalueThreshold', eigenvalueThreshold)
        if numPCA:
            node.put('numPCA', numPCA)
        if showEigenvalues:
            node.put('showEigenvalues', showEigenvalues)
        if subtractMeanImage:
            node.put('subtractMeanImage', subtractMeanImage)

        self.nodes.append(node)

    def add_write_rgb(self,
        red: int = None,
        green: int = None,
        blue: int = None,
        formatName = None,
        file = None
        ):
        '''
        Creates an RGB image from three source bands.

        Parameters
        ----------
        red : int
            The zero-based index of the red band.
        green : int
            The zero-based index of the green band.
        blue : int
            The zero-based index of the blue band.
        formatName : java.lang.String
            Default 'png'
        file : java.io.File
            The file to which the image is written.
        '''

        node = Node('WriteRGB')

        if red:
            node.put('red', red)
        if green:
            node.put('green', green)
        if blue:
            node.put('blue', blue)
        if formatName:
            node.put('formatName', formatName)
        if file:
            node.put('file', file)

        self.nodes.append(node)

    def add_bands_extractor_op(self,
        sourceBandNames = None,
        sourceMaskNames = None
        ):
        '''
        Creates a new product out of the source product containing only the indexes bands given

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The source bands for the computation.
        sourceMaskNames : java.lang.String[]
            The source masks for the computation.
        '''

        node = Node('BandsExtractorOp')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if sourceMaskNames:
            node.put('sourceMaskNames', sourceMaskNames)

        self.nodes.append(node)

    def add_image_filter(self,
        sourceBandNames = None,
        selectedFilterName = None,
        userDefinedKernelFile = None
        ):
        '''
        Common Image Processing Filters

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        selectedFilterName : java.lang.String
        userDefinedKernelFile : java.io.File
            The kernel file
        '''

        node = Node('Image-Filter')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if selectedFilterName:
            node.put('selectedFilterName', selectedFilterName)
        if userDefinedKernelFile:
            node.put('userDefinedKernelFile', userDefinedKernelFile)

        self.nodes.append(node)

    def add_band_maths(self,
        targetBandDescriptors = None,
        variables = None
        ):
        '''
        Create a product with one or more bands using mathematical expressions.

        Parameters
        ----------
        targetBandDescriptors : org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor[]
            List of descriptors defining the target bands.
        variables : org.esa.snap.core.gpf.common.BandMathsOp$Variable[]
            List of variables which can be used within the expressions.
        '''

        node = Node('BandMaths')

        if targetBandDescriptors:
            node.put('targetBandDescriptors', targetBandDescriptors)
        if variables:
            node.put('variables', variables)

        self.nodes.append(node)

    def add_meris_land_classification(self,
        copyAllTiePoints: bool = None
        ):
        '''
        MERIS L2 land/water reclassification.

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        '''

        node = Node('Meris.LandClassification')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)

        self.nodes.append(node)

    def add_msavi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        slope: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        This retrieves the Modified Soil Adjusted Vegetation Index (MSAVI).

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the RED source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        slope : float
            The soil line slope.
            Default '0.5F'
        redSourceBand : java.lang.String
            The red band for the MSAVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the MSAVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('MsaviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if slope:
            node.put('slope', slope)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_meris_mod08_aerosol(self,
        copyAllTiePoints: bool = None,
        auxdataDir = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        auxdataDir : java.lang.String
        '''

        node = Node('Meris.Mod08Aerosol')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if auxdataDir:
            node.put('auxdataDir', auxdataDir)

        self.nodes.append(node)

    def add_cloud_prob(self
        ):
        '''
        Applies a clear sky conservative cloud detection algorithm.

        Parameters
        ----------
        '''

        node = Node('CloudProb')


        self.nodes.append(node)

    def add_pdu_stitching(self,
        sourceProductPaths = None,
        targetDir = None
        ):
        '''
        Stitches multiple SLSTR L1B product dissemination units (PDUs) of the same orbit to a single product.

        Parameters
        ----------
        sourceProductPaths : java.lang.String[]
            A comma-separated list of file paths specifying the product dissemination units.
            Each path may contain the wildcards '**' (matches recursively any directory),
            '*' (matches any character sequence in path names) and
            '?' (matches any single character).
            If not given, the parameter 'sourceProducts' must be provided.
        targetDir : java.io.File
            The directory to which the stitched product shall be written.
            Within this directory, a folder of the SLSTR L1B naming format will be created.
            If no target directory is given, the product will be written to the user directory.
        '''

        node = Node('PduStitching')

        if sourceProductPaths:
            node.put('sourceProductPaths', sourceProductPaths)
        if targetDir:
            node.put('targetDir', targetDir)

        self.nodes.append(node)

    def add_thermal_noise_removal(self,
        selectedPolarisations = None,
        removeThermalNoise = None,
        outputNoise = None,
        reIntroduceThermalNoise = None
        ):
        '''
        Removes thermal noise from products

        Parameters
        ----------
        selectedPolarisations : java.lang.String[]
            The list of polarisations
        removeThermalNoise : java.lang.Boolean
            Remove thermal noise
            Default 'true'
        outputNoise : java.lang.Boolean
            Output noise
            Default 'false'
        reIntroduceThermalNoise : java.lang.Boolean
            Re-introduce thermal noise
            Default 'false'
        '''

        node = Node('ThermalNoiseRemoval')

        if selectedPolarisations:
            node.put('selectedPolarisations', selectedPolarisations)
        if removeThermalNoise:
            node.put('removeThermalNoise', removeThermalNoise)
        if outputNoise:
            node.put('outputNoise', outputNoise)
        if reIntroduceThermalNoise:
            node.put('reIntroduceThermalNoise', reIntroduceThermalNoise)

        self.nodes.append(node)

    def add_simulate_amplitude(self,
        orbitDegree: int = None,
        demName = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        simAmpBandName = None
        ):
        '''
        Simulate amplitude based on DEM

        Parameters
        ----------
        orbitDegree : int
            Degree of orbit interpolation polynomial
            Default '3'
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        simAmpBandName : java.lang.String
            Simulated amplitude band name.
            Default 'sim_amp'
        '''

        node = Node('SimulateAmplitude')

        if orbitDegree:
            node.put('orbitDegree', orbitDegree)
        if demName:
            node.put('demName', demName)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if simAmpBandName:
            node.put('simAmpBandName', simAmpBandName)

        self.nodes.append(node)

    def add_merge(self,
        includes = None,
        excludes = None,
        geographicError: float = None
        ):
        '''
        Allows merging of several source products by using specified 'master' as reference product.

        Parameters
        ----------
        includes : org.esa.snap.core.gpf.common.MergeOp$NodeDescriptor[]
            Defines nodes to be included in the master product. If no includes are provided, all nodes are copied.
        excludes : org.esa.snap.core.gpf.common.MergeOp$NodeDescriptor[]
            Defines nodes to be excluded from the target product. Excludes have precedence above includes.
        geographicError : float
            Defines the maximum lat/lon error in degree between the products. If set to NaN no check for compatible geographic boundary is performed
            Default '1.0E-5f'
        '''

        node = Node('Merge')

        if includes:
            node.put('includes', includes)
        if excludes:
            node.put('excludes', excludes)
        if geographicError:
            node.put('geographicError', geographicError)

        self.nodes.append(node)

    def add_coregistration_op(self,
        masterSourceBand = None,
        slaveSourceBand = None,
        levels: int = None,
        rank: int = None,
        iterations: int = None,
        radius = None
        ):
        '''
        Coregisters two rasters, not considering their location

        Parameters
        ----------
        masterSourceBand : java.lang.String
            The master product band
        slaveSourceBand : java.lang.String
            The slave product band
        levels : int
            The number of levels to process the images.
            Default '6'
        rank : int
            Value used to compute the rank.
            Default '4'
        iterations : int
            The number of interations for each level and for each radius.
            Default '2'
        radius : java.lang.String
            The radius integer values splitted by comma.
            Default '32, 28, 24, 20, 16, 12, 8'
        '''

        node = Node('CoregistrationOp')

        if masterSourceBand:
            node.put('masterSourceBand', masterSourceBand)
        if slaveSourceBand:
            node.put('slaveSourceBand', slaveSourceBand)
        if levels:
            node.put('levels', levels)
        if rank:
            node.put('rank', rank)
        if iterations:
            node.put('iterations', iterations)
        if radius:
            node.put('radius', radius)

        self.nodes.append(node)

    def add_enhanced_spectral_diversity(self,
        fineWinWidthStr = None,
        fineWinHeightStr = None,
        fineWinAccAzimuth = None,
        fineWinAccRange = None,
        fineWinOversampling = None,
        xCorrThreshold: float = None,
        cohThreshold: float = None,
        numBlocksPerOverlap: int = None,
        esdEstimator = None,
        weightFunc = None,
        temporalBaselineType = None,
        maxTemporalBaseline: int = None,
        integrationMethod = None,
        doNotWriteTargetBands: bool = None,
        useSuppliedRangeShift: bool = None,
        overallRangeShift: float = None,
        useSuppliedAzimuthShift: bool = None,
        overallAzimuthShift: float = None
        ):
        '''
        Estimate constant range and azimuth offsets for a stack of images

        Parameters
        ----------
        fineWinWidthStr : java.lang.String, ['32', '64', '128', '256', '512', '1024', '2048']
            Default '512'
        fineWinHeightStr : java.lang.String, ['32', '64', '128', '256', '512', '1024', '2048']
            Default '512'
        fineWinAccAzimuth : java.lang.String, ['2', '4', '8', '16', '32', '64']
            Default '16'
        fineWinAccRange : java.lang.String, ['2', '4', '8', '16', '32', '64']
            Default '16'
        fineWinOversampling : java.lang.String, ['32', '64', '128', '256']
            Default '128'
        xCorrThreshold : double
            The peak cross-correlation threshold
            Default '0.1'
        cohThreshold : double
            The coherence threshold for outlier removal
            Default '0.3'
        numBlocksPerOverlap : int
            The number of windows per overlap for ESD
            Default '10'
        esdEstimator : java.lang.String, ['Average', 'Periodogram']
            ESD estimator used for azimuth shift computation
            Default 'Periodogram'
        weightFunc : java.lang.String, ['None', 'Linear', 'Quadratic', 'Inv Quadratic']
            Weight function of the coherence to use for azimuth shift estimation
            Default 'Inv Quadratic'
        temporalBaselineType : java.lang.String, ['Number of images', 'Number of days']
            Baseline type for building the integration network
            Default 'Number of images'
        maxTemporalBaseline : int
            Maximum temporal baseline (in days or number of images depending on the Temporal baseline type) between pairs of images to construct the network. Any number < 1 will generate a network with all of the possible pairs.
            Default '4'
        integrationMethod : java.lang.String, ['L1', 'L2', 'L1 and L2']
            Method used for integrating the shifts network.
            Default 'L1 and L2'
        doNotWriteTargetBands : boolean
            Do not write target bands
            Default 'false'
        useSuppliedRangeShift : boolean
            Use user supplied range shift
            Default 'false'
        overallRangeShift : double
            The overall range shift
            Default '0.0'
        useSuppliedAzimuthShift : boolean
            Use user supplied azimuth shift
            Default 'false'
        overallAzimuthShift : double
            The overall azimuth shift
            Default '0.0'
        '''

        node = Node('Enhanced-Spectral-Diversity')

        if fineWinWidthStr:
            node.put('fineWinWidthStr', fineWinWidthStr)
        if fineWinHeightStr:
            node.put('fineWinHeightStr', fineWinHeightStr)
        if fineWinAccAzimuth:
            node.put('fineWinAccAzimuth', fineWinAccAzimuth)
        if fineWinAccRange:
            node.put('fineWinAccRange', fineWinAccRange)
        if fineWinOversampling:
            node.put('fineWinOversampling', fineWinOversampling)
        if xCorrThreshold:
            node.put('xCorrThreshold', xCorrThreshold)
        if cohThreshold:
            node.put('cohThreshold', cohThreshold)
        if numBlocksPerOverlap:
            node.put('numBlocksPerOverlap', numBlocksPerOverlap)
        if esdEstimator:
            node.put('esdEstimator', esdEstimator)
        if weightFunc:
            node.put('weightFunc', weightFunc)
        if temporalBaselineType:
            node.put('temporalBaselineType', temporalBaselineType)
        if maxTemporalBaseline:
            node.put('maxTemporalBaseline', maxTemporalBaseline)
        if integrationMethod:
            node.put('integrationMethod', integrationMethod)
        if doNotWriteTargetBands:
            node.put('doNotWriteTargetBands', doNotWriteTargetBands)
        if useSuppliedRangeShift:
            node.put('useSuppliedRangeShift', useSuppliedRangeShift)
        if overallRangeShift:
            node.put('overallRangeShift', overallRangeShift)
        if useSuppliedAzimuthShift:
            node.put('useSuppliedAzimuthShift', useSuppliedAzimuthShift)
        if overallAzimuthShift:
            node.put('overallAzimuthShift', overallAzimuthShift)

        self.nodes.append(node)

    def add_ellipsoid_correction_rd(self,
        sourceBandNames = None,
        demName = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        externalDEMApplyEGM = None,
        demResamplingMethod = None,
        imgResamplingMethod = None,
        pixelSpacingInMeter: float = None,
        pixelSpacingInDegree: float = None,
        mapProjection = None,
        alignToStandardGrid: bool = None,
        standardGridOriginX: float = None,
        standardGridOriginY: float = None,
        nodataValueAtSea: bool = None,
        saveDEM: bool = None,
        saveLatLon: bool = None,
        saveIncidenceAngleFromEllipsoid: bool = None,
        saveLocalIncidenceAngle: bool = None,
        saveProjectedLocalIncidenceAngle: bool = None,
        saveSelectedSourceBand: bool = None,
        saveLayoverShadowMask: bool = None,
        outputComplex: bool = None,
        applyRadiometricNormalization: bool = None,
        saveSigmaNought: bool = None,
        saveGammaNought: bool = None,
        saveBetaNought: bool = None,
        incidenceAngleForSigma0 = None,
        incidenceAngleForGamma0 = None,
        auxFile = None,
        externalAuxFile = None
        ):
        '''
        Ellipsoid correction with RD method and average scene height

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        externalDEMApplyEGM : java.lang.Boolean
            Default 'true'
        demResamplingMethod : java.lang.String, ['NEAREST_NEIGHBOUR', 'BILINEAR_INTERPOLATION', 'CUBIC_CONVOLUTION', 'BISINC_5_POINT_INTERPOLATION', 'BISINC_11_POINT_INTERPOLATION', 'BISINC_21_POINT_INTERPOLATION', 'BICUBIC_INTERPOLATION', 'DELAUNAY_INTERPOLATION']
            Default 'BILINEAR_INTERPOLATION'
        imgResamplingMethod : java.lang.String, ['NEAREST_NEIGHBOUR', 'BILINEAR_INTERPOLATION', 'CUBIC_CONVOLUTION', 'BISINC_5_POINT_INTERPOLATION', 'BISINC_11_POINT_INTERPOLATION', 'BISINC_21_POINT_INTERPOLATION', 'BICUBIC_INTERPOLATION']
            Default 'BILINEAR_INTERPOLATION'
        pixelSpacingInMeter : double
            The pixel spacing in meters
            Default '0'
        pixelSpacingInDegree : double
            The pixel spacing in degrees
            Default '0'
        mapProjection : java.lang.String
            The coordinate reference system in well known text format
            Default 'WGS84(DD)'
        alignToStandardGrid : boolean
            Force the image grid to be aligned with a specific point
            Default 'false'
        standardGridOriginX : double
            x-coordinate of the standard grid's origin point
            Default '0'
        standardGridOriginY : double
            y-coordinate of the standard grid's origin point
            Default '0'
        nodataValueAtSea : boolean
            Mask the sea with no data value (faster)
            Default 'true'
        saveDEM : boolean
            Default 'false'
        saveLatLon : boolean
            Default 'false'
        saveIncidenceAngleFromEllipsoid : boolean
            Default 'false'
        saveLocalIncidenceAngle : boolean
            Default 'false'
        saveProjectedLocalIncidenceAngle : boolean
            Default 'false'
        saveSelectedSourceBand : boolean
            Default 'true'
        saveLayoverShadowMask : boolean
            Default 'false'
        outputComplex : boolean
            Default 'false'
        applyRadiometricNormalization : boolean
            Default 'false'
        saveSigmaNought : boolean
            Default 'false'
        saveGammaNought : boolean
            Default 'false'
        saveBetaNought : boolean
            Default 'false'
        incidenceAngleForSigma0 : java.lang.String, ['Use incidence angle from Ellipsoid', 'Use local incidence angle from DEM', 'Use projected local incidence angle from DEM']
            Default 'Use projected local incidence angle from DEM'
        incidenceAngleForGamma0 : java.lang.String, ['Use incidence angle from Ellipsoid', 'Use local incidence angle from DEM', 'Use projected local incidence angle from DEM']
            Default 'Use projected local incidence angle from DEM'
        auxFile : java.lang.String, ['Latest Auxiliary File', 'Product Auxiliary File', 'External Auxiliary File']
            The auxiliary file
            Default 'Latest Auxiliary File'
        externalAuxFile : java.io.File
            The antenne elevation pattern gain auxiliary data file.
        '''

        node = Node('Ellipsoid-Correction-RD')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if demName:
            node.put('demName', demName)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if externalDEMApplyEGM:
            node.put('externalDEMApplyEGM', externalDEMApplyEGM)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if imgResamplingMethod:
            node.put('imgResamplingMethod', imgResamplingMethod)
        if pixelSpacingInMeter:
            node.put('pixelSpacingInMeter', pixelSpacingInMeter)
        if pixelSpacingInDegree:
            node.put('pixelSpacingInDegree', pixelSpacingInDegree)
        if mapProjection:
            node.put('mapProjection', mapProjection)
        if alignToStandardGrid:
            node.put('alignToStandardGrid', alignToStandardGrid)
        if standardGridOriginX:
            node.put('standardGridOriginX', standardGridOriginX)
        if standardGridOriginY:
            node.put('standardGridOriginY', standardGridOriginY)
        if nodataValueAtSea:
            node.put('nodataValueAtSea', nodataValueAtSea)
        if saveDEM:
            node.put('saveDEM', saveDEM)
        if saveLatLon:
            node.put('saveLatLon', saveLatLon)
        if saveIncidenceAngleFromEllipsoid:
            node.put('saveIncidenceAngleFromEllipsoid', saveIncidenceAngleFromEllipsoid)
        if saveLocalIncidenceAngle:
            node.put('saveLocalIncidenceAngle', saveLocalIncidenceAngle)
        if saveProjectedLocalIncidenceAngle:
            node.put('saveProjectedLocalIncidenceAngle', saveProjectedLocalIncidenceAngle)
        if saveSelectedSourceBand:
            node.put('saveSelectedSourceBand', saveSelectedSourceBand)
        if saveLayoverShadowMask:
            node.put('saveLayoverShadowMask', saveLayoverShadowMask)
        if outputComplex:
            node.put('outputComplex', outputComplex)
        if applyRadiometricNormalization:
            node.put('applyRadiometricNormalization', applyRadiometricNormalization)
        if saveSigmaNought:
            node.put('saveSigmaNought', saveSigmaNought)
        if saveGammaNought:
            node.put('saveGammaNought', saveGammaNought)
        if saveBetaNought:
            node.put('saveBetaNought', saveBetaNought)
        if incidenceAngleForSigma0:
            node.put('incidenceAngleForSigma0', incidenceAngleForSigma0)
        if incidenceAngleForGamma0:
            node.put('incidenceAngleForGamma0', incidenceAngleForGamma0)
        if auxFile:
            node.put('auxFile', auxFile)
        if externalAuxFile:
            node.put('externalAuxFile', externalAuxFile)

        self.nodes.append(node)

    def add_s_m_dielectric_modeling(self,
        modelToUse = None,
        minSM: float = None,
        maxSM: float = None,
        outputRDC: bool = None,
        outputLandCover: bool = None,
        effectiveSoilTemperature: float = None
        ):
        '''
        Performs SM inversion using dielectric model

        Parameters
        ----------
        modelToUse : java.lang.String, ['Hallikainen', 'Mironov']
            Choice of dielectric models for SM inversion
            Default 'Hallikainen'
        minSM : double
            Minimum soil moisture value
            Default '0.0'
        maxSM : double
            Maximum soil moisture value
            Default '0.55'
        outputRDC : boolean
            Optional RDC in output
            Default 'true'
        outputLandCover : boolean
            Optional LandCover in output
            Default 'true'
        effectiveSoilTemperature : double
            Effective soil temperature
            Default '18.0'
        '''

        node = Node('SM-Dielectric-Modeling')

        if modelToUse:
            node.put('modelToUse', modelToUse)
        if minSM:
            node.put('minSM', minSM)
        if maxSM:
            node.put('maxSM', maxSM)
        if outputRDC:
            node.put('outputRDC', outputRDC)
        if outputLandCover:
            node.put('outputLandCover', outputLandCover)
        if effectiveSoilTemperature:
            node.put('effectiveSoilTemperature', effectiveSoilTemperature)

        self.nodes.append(node)

    def add_ci_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        greenFactor: float = None,
        redSourceBand = None,
        greenSourceBand = None
        ):
        '''
        Colour Index  was developed to differentiate soils in the field. It gives complementary information with the BI and the NDVI.

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        greenFactor : float
            The value of the green source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the CI computation. If not provided, the operator will try to find the best fitting band.
        greenSourceBand : java.lang.String
            The green band for the CI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('CiOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if greenFactor:
            node.put('greenFactor', greenFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if greenSourceBand:
            node.put('greenSourceBand', greenSourceBand)

        self.nodes.append(node)

    def add_ppe_filtering(self,
        cutOff: float = None,
        numberOfMAD: float = None,
        validExpression = None
        ):
        '''
        Performs Prompt Particle Event (PPE) filtering on OLCI L1B

        Parameters
        ----------
        cutOff : double
            Minimum threshold to differentiate with the neighboring pixels.
            Default '0.7'
        numberOfMAD : double
            Multiplier of MAD (Median Absolute Deviation) used for the threshold.
            Default '10'
        validExpression : java.lang.String
            An expression to filter which pixel are considered.
            Default 'not quality_flags_land'
        '''

        node = Node('PpeFiltering')

        if cutOff:
            node.put('cutOff', cutOff)
        if numberOfMAD:
            node.put('numberOfMAD', numberOfMAD)
        if validExpression:
            node.put('validExpression', validExpression)

        self.nodes.append(node)

    def add_mci_s2(self,
        lowerBaselineBandName = None,
        upperBaselineBandName = None,
        signalBandName = None,
        lineHeightBandName = None,
        slope: bool = None,
        slopeBandName = None,
        maskExpression = None,
        cloudCorrectionFactor: float = None,
        invalidMciValue: float = None
        ):
        '''
        Computes maximum chlorophyll index (MCI) for Sentinel-2 MSI.

        Parameters
        ----------
        lowerBaselineBandName : java.lang.String
            The name for the lower wavelength band defining the baseline
        upperBaselineBandName : java.lang.String
            The name of the upper wavelength band defining the baseline
        signalBandName : java.lang.String
             The name of the signal band, i.e. the band for which the baseline height is calculated
        lineHeightBandName : java.lang.String
            The name of the MCI band in the target product
        slope : boolean
            Activates or deactivates calculating the slope parameter
            Default 'true'
        slopeBandName : java.lang.String
            The name of the slope band in the target product
        maskExpression : java.lang.String
            A ROI-mask expression used to identify pixels of interest
        cloudCorrectionFactor : float
            The cloud correction factor used during calculation
            Default '1.005'
        invalidMciValue : float
            Value used to fill invalid MCI pixels
            Default 'NaN'
        '''

        node = Node('Mci.s2')

        if lowerBaselineBandName:
            node.put('lowerBaselineBandName', lowerBaselineBandName)
        if upperBaselineBandName:
            node.put('upperBaselineBandName', upperBaselineBandName)
        if signalBandName:
            node.put('signalBandName', signalBandName)
        if lineHeightBandName:
            node.put('lineHeightBandName', lineHeightBandName)
        if slope:
            node.put('slope', slope)
        if slopeBandName:
            node.put('slopeBandName', slopeBandName)
        if maskExpression:
            node.put('maskExpression', maskExpression)
        if cloudCorrectionFactor:
            node.put('cloudCorrectionFactor', cloudCorrectionFactor)
        if invalidMciValue:
            node.put('invalidMciValue', invalidMciValue)

        self.nodes.append(node)

    def add_phase_to_displacement(self
        ):
        '''
        Phase To Displacement Conversion along LOS

        Parameters
        ----------
        '''

        node = Node('PhaseToDisplacement')


        self.nodes.append(node)

    def add_range_filter(self,
        fftLength: int = None,
        alphaHamming: float = None,
        nlMean: int = None,
        snrThresh: float = None,
        ovsmpFactor: int = None,
        doWeightCorrel: bool = None
        ):
        '''
        Range Filter

        Parameters
        ----------
        fftLength : int, ['8', '16', '32', '64', '128', '256', '512', '1024']
            Length of filtering window
            Default '8'
        alphaHamming : float, ['0.5', '0.75', '0.8', '0.9', '1']
            Weight for Hamming filter (1 is rectangular window)
            Default '0.75'
        nlMean : int, ['5', '10', '15', '20', '25']
            Input value for (walking) mean averaging to reduce noise.
            Default '15'
        snrThresh : float, ['3', '4', '5', '6', '7']
            Threshold on SNR for peak estimation
            Default '5'
        ovsmpFactor : int, ['1', '2', '4']
            Oversampling factor (in range only).
            Default '1'
        doWeightCorrel : boolean, ['true', 'false']
            Use weight values to bias higher frequencies
            Default 'off'
        '''

        node = Node('RangeFilter')

        if fftLength:
            node.put('fftLength', fftLength)
        if alphaHamming:
            node.put('alphaHamming', alphaHamming)
        if nlMean:
            node.put('nlMean', nlMean)
        if snrThresh:
            node.put('snrThresh', snrThresh)
        if ovsmpFactor:
            node.put('ovsmpFactor', ovsmpFactor)
        if doWeightCorrel:
            node.put('doWeightCorrel', doWeightCorrel)

        self.nodes.append(node)

    def add_biophysical_op(self,
        sensor = None,
        computeLAI: bool = None,
        computeFapar: bool = None,
        computeFcover: bool = None,
        computeCab: bool = None,
        computeCw: bool = None
        ):
        '''
        The 'Biophysical Processor' operator retrieves LAI from atmospherically corrected Sentinel-2 products

        Parameters
        ----------
        sensor : java.lang.String, ['S2A', 'S2B']
            Sensor
            Default 'S2A'
        computeLAI : boolean
            Compute LAI (Leaf Area Index)
            Default 'true'
        computeFapar : boolean
            Compute FAPAR (Fraction of Absorbed Photosynthetically Active Radiation)
            Default 'true'
        computeFcover : boolean
            Compute FVC (Fraction of Vegetation Cover)
            Default 'true'
        computeCab : boolean
            Compute Cab (Chlorophyll content in the leaf)
            Default 'true'
        computeCw : boolean
            Compute Cw (Canopy Water Content)
            Default 'true'
        '''

        node = Node('BiophysicalOp')

        if sensor:
            node.put('sensor', sensor)
        if computeLAI:
            node.put('computeLAI', computeLAI)
        if computeFapar:
            node.put('computeFapar', computeFapar)
        if computeFcover:
            node.put('computeFcover', computeFcover)
        if computeCab:
            node.put('computeCab', computeCab)
        if computeCw:
            node.put('computeCw', computeCw)

        self.nodes.append(node)

    def add_stamps_export(self,
        targetFolder = None,
        psiFormat = None
        ):
        '''
        Export data for StaMPS processing

        Parameters
        ----------
        targetFolder : java.io.File
            The output folder to which the data product is written.
        psiFormat : java.lang.Boolean
            Format for PSI or SBAS
            Default 'true'
        '''

        node = Node('StampsExport')

        if targetFolder:
            node.put('targetFolder', targetFolder)
        if psiFormat:
            node.put('psiFormat', psiFormat)

        self.nodes.append(node)

    def add_rayleigh_correction(self,
        sourceBandNames = None,
        computeTaur: bool = None,
        computeRBrr: bool = None,
        computeRtoaNg: bool = None,
        computeRtoa: bool = None,
        addAirMass: bool = None,
        s2MsiTargetResolution: int = None,
        s2MsiSeaLevelPressure: float = None,
        s2MsiOzone: float = None
        ):
        '''
        Performs radiometric corrections on OLCI, MERIS L1B and S2 MSI L1C data products.

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The source bands for the computation.
        computeTaur : boolean
            Default 'false'
        computeRBrr : boolean
            Default 'true'
        computeRtoaNg : boolean
            Default 'false'
        computeRtoa : boolean
            Default 'false'
        addAirMass : boolean
            Default 'false'
        s2MsiTargetResolution : int, ['10', '20', '60']
            Default '20'
        s2MsiSeaLevelPressure : double
            Default '1013.25'
        s2MsiOzone : double
            Default '300.0'
        '''

        node = Node('RayleighCorrection')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if computeTaur:
            node.put('computeTaur', computeTaur)
        if computeRBrr:
            node.put('computeRBrr', computeRBrr)
        if computeRtoaNg:
            node.put('computeRtoaNg', computeRtoaNg)
        if computeRtoa:
            node.put('computeRtoa', computeRtoa)
        if addAirMass:
            node.put('addAirMass', addAirMass)
        if s2MsiTargetResolution:
            node.put('s2MsiTargetResolution', s2MsiTargetResolution)
        if s2MsiSeaLevelPressure:
            node.put('s2MsiSeaLevelPressure', s2MsiSeaLevelPressure)
        if s2MsiOzone:
            node.put('s2MsiOzone', s2MsiOzone)

        self.nodes.append(node)

    def add_resample(self,
        referenceBandName = None,
        targetWidth = None,
        targetHeight = None,
        targetResolution = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        flagDownsamplingMethod = None,
        resamplingPreset = None,
        bandResamplings = None,
        resampleOnPyramidLevels: bool = None
        ):
        '''
        Resampling of a multi-size source product to a single-size target product.

        Parameters
        ----------
        referenceBandName : java.lang.String
            The name of the reference band. All other bands will be re-sampled to match its size and resolution. Either this or targetResolutionor targetWidth and targetHeight must be set.
        targetWidth : java.lang.Integer
            The width that all bands of the target product shall have. If this is set, targetHeight must be set, too. Either this and targetHeight or referenceBand or targetResolution must be set.
        targetHeight : java.lang.Integer
            The height that all bands of the target product shall have. If this is set, targetWidth must be set, too. Either this and targetWidth or referenceBand or targetResolution must be set.
        targetResolution : java.lang.Integer
            The resolution that all bands of the target product shall have. The same value will be applied to scale image widths and heights. Either this or referenceBand or targetwidth and targetHeight must be set.
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        flagDownsamplingMethod : java.lang.String, ['First', 'FlagAnd', 'FlagOr', 'FlagMedianAnd', 'FlagMedianOr']
            The method used for aggregation (downsampling to a coarser resolution) of flags.
            Default 'First'
        resamplingPreset : java.lang.String
            The resampling preset. This will over rules the settings for upsampling, downsampling and flagDownsampling.
        bandResamplings : java.lang.String
            The band resamplings. This will over rules the settings for resamplingPreset.
        resampleOnPyramidLevels : boolean
            This setting will increase performance when viewing the image, but accurate resamplings are only retrieved when zooming in on a pixel.
            Default 'true'
        '''

        node = Node('Resample')

        if referenceBandName:
            node.put('referenceBandName', referenceBandName)
        if targetWidth:
            node.put('targetWidth', targetWidth)
        if targetHeight:
            node.put('targetHeight', targetHeight)
        if targetResolution:
            node.put('targetResolution', targetResolution)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if flagDownsamplingMethod:
            node.put('flagDownsamplingMethod', flagDownsamplingMethod)
        if resamplingPreset:
            node.put('resamplingPreset', resamplingPreset)
        if bandResamplings:
            node.put('bandResamplings', bandResamplings)
        if resampleOnPyramidLevels:
            node.put('resampleOnPyramidLevels', resampleOnPyramidLevels)

        self.nodes.append(node)

    def add_offset_tracking(self,
        gridAzimuthSpacing: int = None,
        gridRangeSpacing: int = None,
        registrationWindowWidth = None,
        registrationWindowHeight = None,
        xCorrThreshold: float = None,
        registrationOversampling = None,
        averageBoxSize = None,
        maxVelocity: float = None,
        radius: int = None,
        resamplingType = None,
        spatialAverage: bool = None,
        fillHoles: bool = None,
        roiVector = None
        ):
        '''
        Create velocity vectors from offset tracking

        Parameters
        ----------
        gridAzimuthSpacing : int
            The output grid azimuth spacing in pixels
            Default '40'
        gridRangeSpacing : int
            The output grid range spacing in pixels
            Default '40'
        registrationWindowWidth : java.lang.String, ['32', '64', '128', '256', '512', '1024', '2048']
            Default '128'
        registrationWindowHeight : java.lang.String, ['32', '64', '128', '256', '512', '1024', '2048']
            Default '128'
        xCorrThreshold : double
            The cross-correlation threshold
            Default '0.1'
        registrationOversampling : java.lang.String, ['2', '4', '8', '16', '32', '64', '128', '256', '512']
            Default '16'
        averageBoxSize : java.lang.String, ['3', '5', '9', '11']
            Default '5'
        maxVelocity : double
            The threshold for eliminating invalid GCPs
            Default '5.0'
        radius : int
            Radius for Hole-Filling
            Default '4'
        resamplingType : java.lang.String, ['NEAREST_NEIGHBOUR', 'BILINEAR_INTERPOLATION', 'BICUBIC_INTERPOLATION', 'BISINC_5_POINT_INTERPOLATION', 'CUBIC_CONVOLUTION']
            Methods for velocity interpolation.
            Default 'BICUBIC_INTERPOLATION'
        spatialAverage : boolean
            Default 'true'
        fillHoles : boolean
            Default 'true'
        roiVector : java.lang.String
        '''

        node = Node('Offset-Tracking')

        if gridAzimuthSpacing:
            node.put('gridAzimuthSpacing', gridAzimuthSpacing)
        if gridRangeSpacing:
            node.put('gridRangeSpacing', gridRangeSpacing)
        if registrationWindowWidth:
            node.put('registrationWindowWidth', registrationWindowWidth)
        if registrationWindowHeight:
            node.put('registrationWindowHeight', registrationWindowHeight)
        if xCorrThreshold:
            node.put('xCorrThreshold', xCorrThreshold)
        if registrationOversampling:
            node.put('registrationOversampling', registrationOversampling)
        if averageBoxSize:
            node.put('averageBoxSize', averageBoxSize)
        if maxVelocity:
            node.put('maxVelocity', maxVelocity)
        if radius:
            node.put('radius', radius)
        if resamplingType:
            node.put('resamplingType', resamplingType)
        if spatialAverage:
            node.put('spatialAverage', spatialAverage)
        if fillHoles:
            node.put('fillHoles', fillHoles)
        if roiVector:
            node.put('roiVector', roiVector)

        self.nodes.append(node)

    def add_ndpi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        greenFactor: float = None,
        mirFactor: float = None,
        greenSourceBand = None,
        mirSourceBand = None
        ):
        '''
        The normalized differential pond index, combines the short-wave infrared band-I and the green band

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        greenFactor : float
            The value of the green source band is multiplied by this value.
            Default '1.0F'
        mirFactor : float
            The value of the MIR source band is multiplied by this value.
            Default '1.0F'
        greenSourceBand : java.lang.String
            The green band for the NDPI computation. If not provided, the operator will try to find the best fitting band.
        mirSourceBand : java.lang.String
            The mid-infrared band for the NDPI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('NdpiOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if greenFactor:
            node.put('greenFactor', greenFactor)
        if mirFactor:
            node.put('mirFactor', mirFactor)
        if greenSourceBand:
            node.put('greenSourceBand', greenSourceBand)
        if mirSourceBand:
            node.put('mirSourceBand', mirSourceBand)

        self.nodes.append(node)

    def add_dem_assisted_coregistration(self,
        demName = None,
        demResamplingMethod = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        resamplingType = None,
        tileExtensionPercent: int = None,
        maskOutAreaWithoutElevation: bool = None,
        outputRangeAzimuthOffset: bool = None
        ):
        '''
        Orbit and DEM based co-registration

        Parameters
        ----------
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        demResamplingMethod : java.lang.String
            Default 'BICUBIC_INTERPOLATION'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        resamplingType : java.lang.String
            The method to be used when resampling the slave grid onto the master grid.
            Default 'BISINC_5_POINT_INTERPOLATION'
        tileExtensionPercent : int
            Define tile extension percentage.
            Default '50'
        maskOutAreaWithoutElevation : boolean
            Default 'true'
        outputRangeAzimuthOffset : boolean
            Default 'false'
        '''

        node = Node('DEM-Assisted-Coregistration')

        if demName:
            node.put('demName', demName)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if resamplingType:
            node.put('resamplingType', resamplingType)
        if tileExtensionPercent:
            node.put('tileExtensionPercent', tileExtensionPercent)
        if maskOutAreaWithoutElevation:
            node.put('maskOutAreaWithoutElevation', maskOutAreaWithoutElevation)
        if outputRangeAzimuthOffset:
            node.put('outputRangeAzimuthOffset', outputRangeAzimuthOffset)

        self.nodes.append(node)

    def add_alos_deskewing(self,
        sourceBandNames = None,
        demName = None
        ):
        '''
        Deskewing ALOS product

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        '''

        node = Node('ALOS-Deskewing')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if demName:
            node.put('demName', demName)

        self.nodes.append(node)

    def add_oil_spill_clustering(self,
        minClusterSizeInKm2: float = None
        ):
        '''
        Remove small clusters from detected area.

        Parameters
        ----------
        minClusterSizeInKm2 : double
            Minimum cluster size
            Default '0.1'
        '''

        node = Node('Oil-Spill-Clustering')

        if minClusterSizeInKm2:
            node.put('minClusterSizeInKm2', minClusterSizeInKm2)

        self.nodes.append(node)

    def add_forest_cover_change_op(self,
        forestCoverPercentage: float = None,
        landCoverName = None,
        landCoverMapIndices = None,
        mergingCostCriterion = None,
        regionMergingCriterion = None,
        totalIterationsForSecondSegmentation: int = None,
        threshold: float = None,
        spectralWeight: float = None,
        shapeWeight: float = None,
        degreesOfFreedom: float = None,
        currentProductSourceMaskFile = None,
        previousProductSourceMaskFile = None
        ):
        '''
        Creates forest change masks out of two source products

        Parameters
        ----------
        forestCoverPercentage : float
            Specifies the percentage of forest cover per segment
            Default '95.0'
        landCoverName : java.lang.String
            Default 'CCILandCover-2015'
        landCoverMapIndices : java.lang.String
            The indices of forest color from the new added land cover map
            Default '40, 50, 60, 61, 62, 70, 71, 72, 80, 81, 82, 90, 100, 110, 160, 170'
        mergingCostCriterion : java.lang.String, ['Spring', 'Baatz & Schape', 'Full Lamda Schedule']
            The method to compute the region merging.
            Default 'Spring'
        regionMergingCriterion : java.lang.String, ['Best Fitting', 'Local Mutual Best Fitting']
            The method to check the region merging.
            Default 'Local Mutual Best Fitting'
        totalIterationsForSecondSegmentation : int
            The total number of iterations.
            Default '10'
        threshold : float
            The threshold.
            Default '5.0'
        spectralWeight : float
            The spectral weight.
            Default '0.5'
        shapeWeight : float
            The shape weight.
            Default '0.5'
        degreesOfFreedom : double
            Degrees of freedom used for the Chi distribution trimming process
            Default '3.3'
        currentProductSourceMaskFile : java.io.File
            A binary raster file to be added as mask to the output product
        previousProductSourceMaskFile : java.io.File
            A binary raster file to be added as mask to the output product
        '''

        node = Node('ForestCoverChangeOp')

        if forestCoverPercentage:
            node.put('forestCoverPercentage', forestCoverPercentage)
        if landCoverName:
            node.put('landCoverName', landCoverName)
        if landCoverMapIndices:
            node.put('landCoverMapIndices', landCoverMapIndices)
        if mergingCostCriterion:
            node.put('mergingCostCriterion', mergingCostCriterion)
        if regionMergingCriterion:
            node.put('regionMergingCriterion', regionMergingCriterion)
        if totalIterationsForSecondSegmentation:
            node.put('totalIterationsForSecondSegmentation', totalIterationsForSecondSegmentation)
        if threshold:
            node.put('threshold', threshold)
        if spectralWeight:
            node.put('spectralWeight', spectralWeight)
        if shapeWeight:
            node.put('shapeWeight', shapeWeight)
        if degreesOfFreedom:
            node.put('degreesOfFreedom', degreesOfFreedom)
        if currentProductSourceMaskFile:
            node.put('currentProductSourceMaskFile', currentProductSourceMaskFile)
        if previousProductSourceMaskFile:
            node.put('previousProductSourceMaskFile', previousProductSourceMaskFile)

        self.nodes.append(node)

    def add_cross_channel_snr_correction(self,
        windowSize: int = None
        ):
        '''
        Compute general polarimetric parameters

        Parameters
        ----------
        windowSize : int
            The sliding window size
            Default '5'
        '''

        node = Node('Cross-Channel-SNR-Correction')

        if windowSize:
            node.put('windowSize', windowSize)

        self.nodes.append(node)

    def add_ndwi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        mirFactor: float = None,
        nirFactor: float = None,
        mirSourceBand = None,
        nirSourceBand = None
        ):
        '''
        The Normalized Difference Water Index was developed for the extraction of water features

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        mirFactor : float
            The value of the MIR source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        mirSourceBand : java.lang.String
            The mid-infrared band for the NDWI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the NDWI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('NdwiOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if mirFactor:
            node.put('mirFactor', mirFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if mirSourceBand:
            node.put('mirSourceBand', mirSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_convert_datatype(self,
        sourceBandNames = None,
        targetDataType = None,
        targetScalingStr = None,
        targetNoDataValue = None
        ):
        '''
        Convert product data type

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        targetDataType : java.lang.String, ['int8', 'int16', 'int32', 'uint8', 'uint16', 'uint32', 'float32', 'float64']
            Default 'uint8'
        targetScalingStr : java.lang.String, ['Truncate', 'Linear (slope and intercept)', 'Linear (between 95% clipped histogram)', 'Linear (peak clipped histogram)', 'Logarithmic']
            Default 'Linear (between 95% clipped histogram)'
        targetNoDataValue : java.lang.Double
            Default '0'
        '''

        node = Node('Convert-Datatype')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if targetDataType:
            node.put('targetDataType', targetDataType)
        if targetScalingStr:
            node.put('targetScalingStr', targetScalingStr)
        if targetNoDataValue:
            node.put('targetNoDataValue', targetNoDataValue)

        self.nodes.append(node)

    def add_pca(self,
        sourceBandNames = None,
        componentCount: int = None,
        roiMaskName = None,
        removeNonRoiPixels: bool = None
        ):
        '''
        Performs a Principal Component Analysis.

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The names of the bands being used for the cluster analysis.
        componentCount : int
            The maximum number of principal components to compute.
            Default '-1'
        roiMaskName : java.lang.String
            The name of the ROI mask that should be used.
        removeNonRoiPixels : boolean
            Removes all non-ROI pixels in the target product.
            Default 'false'
        '''

        node = Node('PCA')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if componentCount:
            node.put('componentCount', componentCount)
        if roiMaskName:
            node.put('roiMaskName', roiMaskName)
        if removeNonRoiPixels:
            node.put('removeNonRoiPixels', removeNonRoiPixels)

        self.nodes.append(node)

    def add_speckle_filter(self,
        sourceBandNames = None,
        filter = None,
        filterSizeX: int = None,
        filterSizeY: int = None,
        dampingFactor: int = None,
        estimateENL: bool = None,
        enl: float = None,
        numLooksStr = None,
        windowSize = None,
        targetWindowSizeStr = None,
        sigmaStr = None,
        anSize: int = None
        ):
        '''
        Speckle Reduction

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        filter : java.lang.String, ['None', 'Boxcar', 'Median', 'Frost', 'Gamma Map', 'Lee', 'Refined Lee', 'Lee Sigma', 'IDAN']
            Default 'Lee Sigma'
        filterSizeX : int
            The kernel x dimension
            Default '3'
        filterSizeY : int
            The kernel y dimension
            Default '3'
        dampingFactor : int
            The damping factor (Frost filter only)
            Default '2'
        estimateENL : boolean
            Default 'false'
        enl : double
            The number of looks
            Default '1.0'
        numLooksStr : java.lang.String, ['1', '2', '3', '4']
            Default '1'
        windowSize : java.lang.String, ['5x5', '7x7', '9x9', '11x11', '13x13', '15x15', '17x17']
            Default '7x7'
        targetWindowSizeStr : java.lang.String, ['3x3', '5x5']
            Default '3x3'
        sigmaStr : java.lang.String, ['0.5', '0.6', '0.7', '0.8', '0.9']
            Default '0.9'
        anSize : int
            The Adaptive Neighbourhood size
            Default '50'
        '''

        node = Node('Speckle-Filter')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if filter:
            node.put('filter', filter)
        if filterSizeX:
            node.put('filterSizeX', filterSizeX)
        if filterSizeY:
            node.put('filterSizeY', filterSizeY)
        if dampingFactor:
            node.put('dampingFactor', dampingFactor)
        if estimateENL:
            node.put('estimateENL', estimateENL)
        if enl:
            node.put('enl', enl)
        if numLooksStr:
            node.put('numLooksStr', numLooksStr)
        if windowSize:
            node.put('windowSize', windowSize)
        if targetWindowSizeStr:
            node.put('targetWindowSizeStr', targetWindowSizeStr)
        if sigmaStr:
            node.put('sigmaStr', sigmaStr)
        if anSize:
            node.put('anSize', anSize)

        self.nodes.append(node)

    def add_stored_graph(self,
        file = None
        ):
        '''
        Encapsulates an stored graph into an operator.

        Parameters
        ----------
        file : java.io.File
            The file from which the graph is read.
        '''

        node = Node('StoredGraph')

        if file:
            node.put('file', file)

        self.nodes.append(node)

    def addc2rcc_meris4(self,
        validPixelExpression = None,
        salinity: float = None,
        temperature: float = None,
        ozone: float = None,
        press: float = None,
        TSMfakBpart: float = None,
        TSMfakBwit: float = None,
        CHLexp: float = None,
        CHLfak: float = None,
        thresholdRtosaOOS: float = None,
        thresholdAcReflecOos: float = None,
        thresholdCloudTDown865: float = None,
        atmosphericAuxDataPath = None,
        alternativeNNPath = None,
        netSet = None,
        outputAsRrs: bool = None,
        deriveRwFromPathAndTransmittance: bool = None,
        useEcmwfAuxData: bool = None,
        outputRtoa: bool = None,
        outputRtosaGc: bool = None,
        outputRtosaGcAann: bool = None,
        outputRpath: bool = None,
        outputTdown: bool = None,
        outputTup: bool = None,
        outputAcReflectance: bool = None,
        outputRhown: bool = None,
        outputOos: bool = None,
        outputKd: bool = None,
        outputUncertainties: bool = None
        ):
        '''
        Performs atmospheric correction and IOP retrieval with uncertainties on MERIS L1b data products from the 4th reprocessing.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Defines the pixels which are valid for processing.
            Default '!quality_flags.invalid && (!quality_flags.land || quality_flags.fresh_inland_water)'
        salinity : double
            The value used as salinity for the scene.
            Default '35.0'
        temperature : double
            The value used as temperature for the scene.
            Default '15.0'
        ozone : double
            The value used as ozone if not provided by auxiliary data.
            Default '330'
        press : double
            The surface air pressure at sea level if not provided by auxiliary data.
            Default '1000'
        TSMfakBpart : double
            TSM factor (TSM = TSMfac * iop_btot^TSMexp).
            Default '1.72'
        TSMfakBwit : double
            TSM exponent (TSM = TSMfac * iop_btot^TSMexp).
            Default '3.1'
        CHLexp : double
            Chlorophyll exponent ( CHL = iop_apig^CHLexp * CHLfac).
            Default '1.04'
        CHLfak : double
            Chlorophyll factor ( CHL = iop_apig^CHLexp * CHLfac).
            Default '21.0'
        thresholdRtosaOOS : double
            Threshold for out of scope of nn training dataset flag for gas corrected top-of-atmosphere reflectances.
            Default '0.003'
        thresholdAcReflecOos : double
            Threshold for out of scope of nn training dataset flag for atmospherically corrected reflectances.
            Default '0.1'
        thresholdCloudTDown865 : double
            Threshold for cloud test based on downwelling transmittance @865.
            Default '0.955'
        atmosphericAuxDataPath : java.lang.String
            Path to the atmospheric auxiliary data directory. Use either this or the specified products on the I/O Parameters tab. If the auxiliary data is not available at this path, the data will automatically be downloaded.
        alternativeNNPath : java.lang.String
            Path to an alternative set of neuronal nets. Use this to replace the standard set of neuronal nets with the ones in the given directory.
        netSet : java.lang.String, ['C2RCC-Nets', 'C2X-Nets']
            Set of neuronal nets for algorithm.
            Default 'C2RCC-Nets'
        outputAsRrs : boolean
            Write remote sensing reflectances instead of water leaving reflectances.
            Default 'false'
        deriveRwFromPathAndTransmittance : boolean
            Alternative way of calculating water reflectance. Still experimental.
            Default 'false'
        useEcmwfAuxData : boolean
            If selected, the ECMWF auxiliary data (total_ozone, sea_level_pressure) of the source product is used
            Default 'true'
        outputRtoa : boolean
            Default 'true'
        outputRtosaGc : boolean
            Default 'false'
        outputRtosaGcAann : boolean
            Default 'false'
        outputRpath : boolean
            Default 'false'
        outputTdown : boolean
            Default 'false'
        outputTup : boolean
            Default 'false'
        outputAcReflectance : boolean
            Default 'true'
        outputRhown : boolean
            Default 'true'
        outputOos : boolean
            Default 'false'
        outputKd : boolean
            Default 'true'
        outputUncertainties : boolean
            Default 'true'
        '''

        node = Node('c2rcc.meris4')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if salinity:
            node.put('salinity', salinity)
        if temperature:
            node.put('temperature', temperature)
        if ozone:
            node.put('ozone', ozone)
        if press:
            node.put('press', press)
        if TSMfakBpart:
            node.put('TSMfakBpart', TSMfakBpart)
        if TSMfakBwit:
            node.put('TSMfakBwit', TSMfakBwit)
        if CHLexp:
            node.put('CHLexp', CHLexp)
        if CHLfak:
            node.put('CHLfak', CHLfak)
        if thresholdRtosaOOS:
            node.put('thresholdRtosaOOS', thresholdRtosaOOS)
        if thresholdAcReflecOos:
            node.put('thresholdAcReflecOos', thresholdAcReflecOos)
        if thresholdCloudTDown865:
            node.put('thresholdCloudTDown865', thresholdCloudTDown865)
        if atmosphericAuxDataPath:
            node.put('atmosphericAuxDataPath', atmosphericAuxDataPath)
        if alternativeNNPath:
            node.put('alternativeNNPath', alternativeNNPath)
        if netSet:
            node.put('netSet', netSet)
        if outputAsRrs:
            node.put('outputAsRrs', outputAsRrs)
        if deriveRwFromPathAndTransmittance:
            node.put('deriveRwFromPathAndTransmittance', deriveRwFromPathAndTransmittance)
        if useEcmwfAuxData:
            node.put('useEcmwfAuxData', useEcmwfAuxData)
        if outputRtoa:
            node.put('outputRtoa', outputRtoa)
        if outputRtosaGc:
            node.put('outputRtosaGc', outputRtosaGc)
        if outputRtosaGcAann:
            node.put('outputRtosaGcAann', outputRtosaGcAann)
        if outputRpath:
            node.put('outputRpath', outputRpath)
        if outputTdown:
            node.put('outputTdown', outputTdown)
        if outputTup:
            node.put('outputTup', outputTup)
        if outputAcReflectance:
            node.put('outputAcReflectance', outputAcReflectance)
        if outputRhown:
            node.put('outputRhown', outputRhown)
        if outputOos:
            node.put('outputOos', outputOos)
        if outputKd:
            node.put('outputKd', outputKd)
        if outputUncertainties:
            node.put('outputUncertainties', outputUncertainties)

        self.nodes.append(node)

    def add_add_land_cover(self,
        landCoverNames = None,
        externalFiles = None,
        resamplingMethod = None
        ):
        '''
        Creates a land cover band

        Parameters
        ----------
        landCoverNames : java.lang.String[]
            The land cover model.
            Default 'AAFC Canada Sand Pct'
        externalFiles : java.io.File[]
            The external landcover files.
        resamplingMethod : java.lang.String
            Default 'NEAREST_NEIGHBOUR'
        '''

        node = Node('AddLandCover')

        if landCoverNames:
            node.put('landCoverNames', landCoverNames)
        if externalFiles:
            node.put('externalFiles', externalFiles)
        if resamplingMethod:
            node.put('resamplingMethod', resamplingMethod)

        self.nodes.append(node)

    def add_linear_to_fromd_b(self,
        sourceBandNames = None
        ):
        '''
        Converts bands to/from dB

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        '''

        node = Node('LinearToFromdB')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)

        self.nodes.append(node)

    def add_flh_mci(self,
        preset = None,
        lowerBaselineBandName = None,
        upperBaselineBandName = None,
        signalBandName = None,
        lineHeightBandName = None,
        slope: bool = None,
        slopeBandName = None,
        maskExpression = None,
        cloudCorrectionFactor: float = None,
        invalidFlhMciValue: float = None
        ):
        '''
        Computes fluorescence line height (FLH) or maximum chlorophyll index (MCI).

        Parameters
        ----------
        preset : org.esa.s3tbx.processor.flh_mci.Presets
            Sets default values according to the selected preset. The specific parameters have precedence and override the ones from the preset
            Default 'NONE'
        lowerBaselineBandName : java.lang.String
            The name for the lower wavelength band defining the baseline
        upperBaselineBandName : java.lang.String
            The name of the upper wavelength band defining the baseline
        signalBandName : java.lang.String
             The name of the signal band, i.e. the band for which the baseline height is calculated
        lineHeightBandName : java.lang.String
            The name of the line height band in the target product
        slope : boolean
            Activates or deactivates calculating the slope parameter
            Default 'true'
        slopeBandName : java.lang.String
            The name of the slope band in the target product
        maskExpression : java.lang.String
            A ROI-mask expression used to identify pixels of interest
        cloudCorrectionFactor : float
            The cloud correction factor used during calculation
            Default '1.005'
        invalidFlhMciValue : float
            Value used to fill invalid FLH/MCI pixels
            Default 'NaN'
        '''

        node = Node('FlhMci')

        if preset:
            node.put('preset', preset)
        if lowerBaselineBandName:
            node.put('lowerBaselineBandName', lowerBaselineBandName)
        if upperBaselineBandName:
            node.put('upperBaselineBandName', upperBaselineBandName)
        if signalBandName:
            node.put('signalBandName', signalBandName)
        if lineHeightBandName:
            node.put('lineHeightBandName', lineHeightBandName)
        if slope:
            node.put('slope', slope)
        if slopeBandName:
            node.put('slopeBandName', slopeBandName)
        if maskExpression:
            node.put('maskExpression', maskExpression)
        if cloudCorrectionFactor:
            node.put('cloudCorrectionFactor', cloudCorrectionFactor)
        if invalidFlhMciValue:
            node.put('invalidFlhMciValue', invalidFlhMciValue)

        self.nodes.append(node)

    def add_unmix(self,
        sourceBandNames = None,
        endmembers = None,
        endmemberFile = None,
        unmixingModelName = None,
        abundanceBandNameSuffix = None,
        errorBandNameSuffix = None,
        computeErrorBands: bool = None,
        minBandwidth: float = None
        ):
        '''
        Performs a linear spectral unmixing.

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of spectral bands providing the source spectrum.
        endmembers : org.esa.snap.unmixing.Endmember[]
            The list of endmember spectra. Wavelengths must be given in nanometers.
        endmemberFile : java.io.File
            A text file containing (additional) endmembers in a table. Wavelengths must be given in nanometers.
        unmixingModelName : java.lang.String, ['Unconstrained LSU', 'Constrained LSU', 'Fully Constrained LSU']
            The unmixing model.
            Default 'Constrained LSU'
        abundanceBandNameSuffix : java.lang.String
            The suffix for the generated abundance band names (name = endmember + suffix).
            Default '_abundance'
        errorBandNameSuffix : java.lang.String
            The suffix for the generated error band names (name = source + suffix).
            Default '_error'
        computeErrorBands : boolean
            If 'true', error bands for all source bands will be generated.
            Default 'false'
        minBandwidth : double
            Minimum spectral bandwidth used for endmember wavelength matching.
            Default '10.0'
        '''

        node = Node('Unmix')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if endmembers:
            node.put('endmembers', endmembers)
        if endmemberFile:
            node.put('endmemberFile', endmemberFile)
        if unmixingModelName:
            node.put('unmixingModelName', unmixingModelName)
        if abundanceBandNameSuffix:
            node.put('abundanceBandNameSuffix', abundanceBandNameSuffix)
        if errorBandNameSuffix:
            node.put('errorBandNameSuffix', errorBandNameSuffix)
        if computeErrorBands:
            node.put('computeErrorBands', computeErrorBands)
        if minBandwidth:
            node.put('minBandwidth', minBandwidth)

        self.nodes.append(node)

    def add_tool_adapter_op(self
        ):
        '''
        Tool Adapter Operator

        Parameters
        ----------
        '''

        node = Node('ToolAdapterOp')


        self.nodes.append(node)

    def add_meris_aerosol_merger(self,
        copyAllTiePoints: bool = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        '''

        node = Node('Meris.AerosolMerger')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)

        self.nodes.append(node)

    def add_savi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        soilCorrectionFactor: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        This retrieves the Soil-Adjusted Vegetation Index (SAVI).

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        soilCorrectionFactor : float
            The amount or cover of green vegetation.
            Default '0.5F'
        redSourceBand : java.lang.String
            The red band for the SAVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the SAVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('SaviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if soilCorrectionFactor:
            node.put('soilCorrectionFactor', soilCorrectionFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_deburst_wss(self,
        subSwath = None,
        produceIntensitiesOnly: bool = None,
        average: bool = None
        ):
        '''
        Debursts an ASAR WSS product

        Parameters
        ----------
        subSwath : java.lang.String, ['SS1', 'SS2', 'SS3', 'SS4', 'SS5']
            Default 'SS1'
        produceIntensitiesOnly : boolean
            Default 'false'
        average : boolean
            Default 'false'
        '''

        node = Node('DeburstWSS')

        if subSwath:
            node.put('subSwath', subSwath)
        if produceIntensitiesOnly:
            node.put('produceIntensitiesOnly', produceIntensitiesOnly)
        if average:
            node.put('average', average)

        self.nodes.append(node)

    def addc2rcc_meris(self,
        validPixelExpression = None,
        salinity: float = None,
        temperature: float = None,
        ozone: float = None,
        press: float = None,
        TSMfakBpart: float = None,
        TSMfakBwit: float = None,
        CHLexp: float = None,
        CHLfak: float = None,
        thresholdRtosaOOS: float = None,
        thresholdAcReflecOos: float = None,
        thresholdCloudTDown865: float = None,
        atmosphericAuxDataPath = None,
        alternativeNNPath = None,
        netSet = None,
        outputAsRrs: bool = None,
        deriveRwFromPathAndTransmittance: bool = None,
        useDefaultSolarFlux: bool = None,
        useEcmwfAuxData: bool = None,
        outputRtoa: bool = None,
        outputRtosaGc: bool = None,
        outputRtosaGcAann: bool = None,
        outputRpath: bool = None,
        outputTdown: bool = None,
        outputTup: bool = None,
        outputAcReflectance: bool = None,
        outputRhown: bool = None,
        outputOos: bool = None,
        outputKd: bool = None,
        outputUncertainties: bool = None
        ):
        '''
        Performs atmospheric correction and IOP retrieval with uncertainties on MERIS L1b data products.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Defines the pixels which are valid for processing.
            Default '!l1_flags.INVALID && !l1_flags.LAND_OCEAN'
        salinity : double
            The value used as salinity for the scene.
            Default '35.0'
        temperature : double
            The value used as temperature for the scene.
            Default '15.0'
        ozone : double
            The value used as ozone if not provided by auxiliary data.
            Default '330'
        press : double
            The surface air pressure at sea level if not provided by auxiliary data.
            Default '1000'
        TSMfakBpart : double
            TSM factor (TSM = TSMfac * iop_btot^TSMexp).
            Default '1.72'
        TSMfakBwit : double
            TSM exponent (TSM = TSMfac * iop_btot^TSMexp).
            Default '3.1'
        CHLexp : double
            Chlorophyll exponent ( CHL = iop_apig^CHLexp * CHLfac).
            Default '1.04'
        CHLfak : double
            Chlorophyll factor ( CHL = iop_apig^CHLexp * CHLfac).
            Default '21.0'
        thresholdRtosaOOS : double
            Threshold for out of scope of nn training dataset flag for gas corrected top-of-atmosphere reflectances.
            Default '0.003'
        thresholdAcReflecOos : double
            Threshold for out of scope of nn training dataset flag for atmospherically corrected reflectances.
            Default '0.1'
        thresholdCloudTDown865 : double
            Threshold for cloud test based on downwelling transmittance @865.
            Default '0.955'
        atmosphericAuxDataPath : java.lang.String
            Path to the atmospheric auxiliary data directory. Use either this or the specified products on the I/O Parameters tab. If the auxiliary data is not available at this path, the data will automatically be downloaded.
        alternativeNNPath : java.lang.String
            Path to an alternative set of neuronal nets. Use this to replace the standard set of neuronal nets.
        netSet : java.lang.String, ['C2RCC-Nets', 'C2X-Nets']
            Set of neuronal nets for algorithm.
            Default 'C2RCC-Nets'
        outputAsRrs : boolean
            Write remote sensing reflectances instead of water leaving reflectances.
            Default 'false'
        deriveRwFromPathAndTransmittance : boolean
            Alternative way of calculating water reflectance. Still experimental.
            Default 'false'
        useDefaultSolarFlux : boolean
            If 'false', use solar flux from source product
            Default 'false'
        useEcmwfAuxData : boolean
            If selected, the ECMWF auxiliary data (ozon, air pressure) of the source product is used
            Default 'true'
        outputRtoa : boolean
            Default 'true'
        outputRtosaGc : boolean
            Default 'false'
        outputRtosaGcAann : boolean
            Default 'false'
        outputRpath : boolean
            Default 'false'
        outputTdown : boolean
            Default 'false'
        outputTup : boolean
            Default 'false'
        outputAcReflectance : boolean
            Default 'true'
        outputRhown : boolean
            Default 'true'
        outputOos : boolean
            Default 'false'
        outputKd : boolean
            Default 'true'
        outputUncertainties : boolean
            Default 'true'
        '''

        node = Node('c2rcc.meris')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if salinity:
            node.put('salinity', salinity)
        if temperature:
            node.put('temperature', temperature)
        if ozone:
            node.put('ozone', ozone)
        if press:
            node.put('press', press)
        if TSMfakBpart:
            node.put('TSMfakBpart', TSMfakBpart)
        if TSMfakBwit:
            node.put('TSMfakBwit', TSMfakBwit)
        if CHLexp:
            node.put('CHLexp', CHLexp)
        if CHLfak:
            node.put('CHLfak', CHLfak)
        if thresholdRtosaOOS:
            node.put('thresholdRtosaOOS', thresholdRtosaOOS)
        if thresholdAcReflecOos:
            node.put('thresholdAcReflecOos', thresholdAcReflecOos)
        if thresholdCloudTDown865:
            node.put('thresholdCloudTDown865', thresholdCloudTDown865)
        if atmosphericAuxDataPath:
            node.put('atmosphericAuxDataPath', atmosphericAuxDataPath)
        if alternativeNNPath:
            node.put('alternativeNNPath', alternativeNNPath)
        if netSet:
            node.put('netSet', netSet)
        if outputAsRrs:
            node.put('outputAsRrs', outputAsRrs)
        if deriveRwFromPathAndTransmittance:
            node.put('deriveRwFromPathAndTransmittance', deriveRwFromPathAndTransmittance)
        if useDefaultSolarFlux:
            node.put('useDefaultSolarFlux', useDefaultSolarFlux)
        if useEcmwfAuxData:
            node.put('useEcmwfAuxData', useEcmwfAuxData)
        if outputRtoa:
            node.put('outputRtoa', outputRtoa)
        if outputRtosaGc:
            node.put('outputRtosaGc', outputRtosaGc)
        if outputRtosaGcAann:
            node.put('outputRtosaGcAann', outputRtosaGcAann)
        if outputRpath:
            node.put('outputRpath', outputRpath)
        if outputTdown:
            node.put('outputTdown', outputTdown)
        if outputTup:
            node.put('outputTup', outputTup)
        if outputAcReflectance:
            node.put('outputAcReflectance', outputAcReflectance)
        if outputRhown:
            node.put('outputRhown', outputRhown)
        if outputOos:
            node.put('outputOos', outputOos)
        if outputKd:
            node.put('outputKd', outputKd)
        if outputUncertainties:
            node.put('outputUncertainties', outputUncertainties)

        self.nodes.append(node)

    def add_topsar_split(self,
        subswath = None,
        selectedPolarisations = None,
        firstBurstIndex = None,
        lastBurstIndex = None,
        wktAoi = None
        ):
        '''
        Creates a new product with only the selected subswath

        Parameters
        ----------
        subswath : java.lang.String
            The list of source bands.
        selectedPolarisations : java.lang.String[]
            The list of polarisations
        firstBurstIndex : java.lang.Integer
            The first burst index
            Default '1'
        lastBurstIndex : java.lang.Integer
            The last burst index
            Default '9999'
        wktAoi : java.lang.String
            WKT polygon to be used for selecting bursts
        '''

        node = Node('TOPSAR-Split')

        if subswath:
            node.put('subswath', subswath)
        if selectedPolarisations:
            node.put('selectedPolarisations', selectedPolarisations)
        if firstBurstIndex:
            node.put('firstBurstIndex', firstBurstIndex)
        if lastBurstIndex:
            node.put('lastBurstIndex', lastBurstIndex)
        if wktAoi:
            node.put('wktAoi', wktAoi)

        self.nodes.append(node)

    def add_azimuth_shift_estimation_esd(self,
        cohThreshold: float = None,
        numBlocksPerOverlap: int = None
        ):
        '''
        Estimate azimuth offset for the whole image

        Parameters
        ----------
        cohThreshold : double
            The coherence threshold for outlier removal
            Default '0.15'
        numBlocksPerOverlap : int
            The number of windows per overlap for ESD
            Default '10'
        '''

        node = Node('Azimuth-Shift-Estimation-ESD')

        if cohThreshold:
            node.put('cohThreshold', cohThreshold)
        if numBlocksPerOverlap:
            node.put('numBlocksPerOverlap', numBlocksPerOverlap)

        self.nodes.append(node)

    def add_write(self,
        file = None,
        formatName = None,
        deleteOutputOnFailure: bool = None,
        writeEntireTileRows: bool = None,
        clearCacheAfterRowWrite: bool = None
        ):
        '''
        Writes a data product to a file.

        Parameters
        ----------
        file : java.io.File
            The output file to which the data product is written.
        formatName : java.lang.String
            The name of the output file format.
            Default 'BEAM-DIMAP'
        deleteOutputOnFailure : boolean
            If true, all output files are deleted after a failed write operation.
            Default 'true'
        writeEntireTileRows : boolean
            If true, the write operation waits until an entire tile row is computed.
            Default 'false'
        clearCacheAfterRowWrite : boolean
            If true, the internal tile cache is cleared after a tile row has been written. Ignored if writeEntireTileRows=false.
            Default 'false'
        '''

        node = Node('Write')

        if file:
            node.put('file', file)
        if formatName:
            node.put('formatName', formatName)
        if deleteOutputOnFailure:
            node.put('deleteOutputOnFailure', deleteOutputOnFailure)
        if writeEntireTileRows:
            node.put('writeEntireTileRows', writeEntireTileRows)
        if clearCacheAfterRowWrite:
            node.put('clearCacheAfterRowWrite', clearCacheAfterRowWrite)

        self.nodes.append(node)

    def add_s2tbx_reproject(self,
        wktFile = None,
        crs = None,
        resamplingName = None,
        referencePixelX = None,
        referencePixelY = None,
        easting = None,
        northing = None,
        orientation = None,
        pixelSizeX = None,
        pixelSizeY = None,
        width = None,
        height = None,
        tileSizeX = None,
        tileSizeY = None,
        orthorectify: bool = None,
        elevationModelName = None,
        noDataValue = None,
        includeTiePointGrids: bool = None,
        addDeltaBands: bool = None
        ):
        '''
        Reprojection of a source product to a target Coordinate Reference System.

        Parameters
        ----------
        wktFile : java.io.File
            A file which contains the target Coordinate Reference System in WKT format.
        crs : java.lang.String
            A text specifying the target Coordinate Reference System, either in WKT or as an authority code. For appropriate EPSG authority codes see (www.epsg-registry.org). AUTO authority can be used with code 42001 (UTM), and 42002 (Transverse Mercator) where the scene center is used as reference. Examples: EPSG:4326, AUTO:42001
        resamplingName : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for resampling of floating-point raster data.
            Default 'Nearest'
        referencePixelX : java.lang.Double
            The X-position of the reference pixel.
        referencePixelY : java.lang.Double
            The Y-position of the reference pixel.
        easting : java.lang.Double
            The easting of the reference pixel.
        northing : java.lang.Double
            The northing of the reference pixel.
        orientation : java.lang.Double
            The orientation of the output product (in degree).
            Default '0'
        pixelSizeX : java.lang.Double
            The pixel size in X direction given in CRS units.
        pixelSizeY : java.lang.Double
            The pixel size in Y direction given in CRS units.
        width : java.lang.Integer
            The width of the target product.
        height : java.lang.Integer
            The height of the target product.
        tileSizeX : java.lang.Integer
            The tile size in X direction.
        tileSizeY : java.lang.Integer
            The tile size in Y direction.
        orthorectify : boolean
            Whether the source product should be orthorectified. (Not applicable to all products)
            Default 'false'
        elevationModelName : java.lang.String
            The name of the elevation model for the orthorectification. If not given tie-point data is used.
        noDataValue : java.lang.Double
            The value used to indicate no-data.
        includeTiePointGrids : boolean
            Whether tie-point grids should be included in the output product.
            Default 'true'
        addDeltaBands : boolean
            Whether to add delta longitude and latitude bands.
            Default 'false'
        '''

        node = Node('S2tbx-Reproject')

        if wktFile:
            node.put('wktFile', wktFile)
        if crs:
            node.put('crs', crs)
        if resamplingName:
            node.put('resamplingName', resamplingName)
        if referencePixelX:
            node.put('referencePixelX', referencePixelX)
        if referencePixelY:
            node.put('referencePixelY', referencePixelY)
        if easting:
            node.put('easting', easting)
        if northing:
            node.put('northing', northing)
        if orientation:
            node.put('orientation', orientation)
        if pixelSizeX:
            node.put('pixelSizeX', pixelSizeX)
        if pixelSizeY:
            node.put('pixelSizeY', pixelSizeY)
        if width:
            node.put('width', width)
        if height:
            node.put('height', height)
        if tileSizeX:
            node.put('tileSizeX', tileSizeX)
        if tileSizeY:
            node.put('tileSizeY', tileSizeY)
        if orthorectify:
            node.put('orthorectify', orthorectify)
        if elevationModelName:
            node.put('elevationModelName', elevationModelName)
        if noDataValue:
            node.put('noDataValue', noDataValue)
        if includeTiePointGrids:
            node.put('includeTiePointGrids', includeTiePointGrids)
        if addDeltaBands:
            node.put('addDeltaBands', addDeltaBands)

        self.nodes.append(node)

    def add_snaphu_export(self,
        targetFolder = None,
        statCostMode = None,
        initMethod = None,
        numberOfTileRows: int = None,
        numberOfTileCols: int = None,
        numberOfProcessors: int = None,
        rowOverlap: int = None,
        colOverlap: int = None,
        tileCostThreshold: int = None
        ):
        '''
        Export data and prepare conf file for SNAPHU processing

        Parameters
        ----------
        targetFolder : java.io.File
            The output folder to which the data product is written.
        statCostMode : java.lang.String, ['TOPO', 'DEFO', 'SMOOTH', 'NOSTATCOSTS']
            Size of coherence estimation window in Azimuth direction
            Default 'DEFO'
        initMethod : java.lang.String, ['MST', 'MCF']
            Algorithm used for initialization of the wrapped phase values
            Default 'MST'
        numberOfTileRows : int
            Divide the image into tiles and process in parallel. Set to 1 for single tiled.
            Default '10'
        numberOfTileCols : int
            Divide the image into tiles and process in parallel. Set to 1 for single tiled.
            Default '10'
        numberOfProcessors : int
            Number of concurrent processing threads. Set to 1 for single threaded.
            Default '4'
        rowOverlap : int
            Overlap, in pixels, between neighboring tiles.
            Default '200'
        colOverlap : int
            Overlap, in pixels, between neighboring tiles.
            Default '200'
        tileCostThreshold : int
            Cost threshold to use for determining boundaries of reliable regions
             (long, dimensionless; scaled according to other cost constants).
             Larger cost threshold implies smaller regions---safer, but more expensive computationally.
            Default '500'
        '''

        node = Node('SnaphuExport')

        if targetFolder:
            node.put('targetFolder', targetFolder)
        if statCostMode:
            node.put('statCostMode', statCostMode)
        if initMethod:
            node.put('initMethod', initMethod)
        if numberOfTileRows:
            node.put('numberOfTileRows', numberOfTileRows)
        if numberOfTileCols:
            node.put('numberOfTileCols', numberOfTileCols)
        if numberOfProcessors:
            node.put('numberOfProcessors', numberOfProcessors)
        if rowOverlap:
            node.put('rowOverlap', rowOverlap)
        if colOverlap:
            node.put('colOverlap', colOverlap)
        if tileCostThreshold:
            node.put('tileCostThreshold', tileCostThreshold)

        self.nodes.append(node)

    def add_bi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        greenFactor: float = None,
        redSourceBand = None,
        greenSourceBand = None
        ):
        '''
        The Brightness index represents the average of the brightness of a satellite image.

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        greenFactor : float
            The value of the green source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the BI computation. If not provided, the operator will try to find the best fitting band.
        greenSourceBand : java.lang.String
            The green band for the BI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('BiOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if greenFactor:
            node.put('greenFactor', greenFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if greenSourceBand:
            node.put('greenSourceBand', greenSourceBand)

        self.nodes.append(node)

    def add_demodulate(self
        ):
        '''
        Demodulation and deramping of SLC data

        Parameters
        ----------
        '''

        node = Node('Demodulate')


        self.nodes.append(node)

    def add_generalized_radar_vegetation_index(self,
        windowSize: int = None
        ):
        '''
        Generalized Radar Vegetation Indices generation

        Parameters
        ----------
        windowSize : int
            The sliding window size
            Default '5'
        '''

        node = Node('Generalized-Radar-Vegetation-Index')

        if windowSize:
            node.put('windowSize', windowSize)

        self.nodes.append(node)

    def add_arvi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        blueFactor: float = None,
        nirFactor: float = None,
        gammaParameter: float = None,
        redSourceBand = None,
        blueSourceBand = None,
        nirSourceBand = None
        ):
        '''
        Atmospherically Resistant Vegetation Index belongs to a family of indices with built-in atmospheric corrections.

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the RED source band is multiplied by this value.
            Default '1.0F'
        blueFactor : float
            The value of the BLUE source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        gammaParameter : float
            The gamma parameter is like a weighting function that depends on the aerosol type
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the ARVI computation. If not provided, the operator will try to find the best fitting band.
        blueSourceBand : java.lang.String
            The blue band for the ARVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the ARVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('ArviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if blueFactor:
            node.put('blueFactor', blueFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if gammaParameter:
            node.put('gammaParameter', gammaParameter)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if blueSourceBand:
            node.put('blueSourceBand', blueSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_multi_temporal_speckle_filter(self,
        sourceBandNames = None,
        filter = None,
        filterSizeX: int = None,
        filterSizeY: int = None,
        dampingFactor: int = None,
        estimateENL: bool = None,
        enl: float = None,
        numLooksStr = None,
        windowSize = None,
        targetWindowSizeStr = None,
        sigmaStr = None,
        anSize: int = None
        ):
        '''
        Speckle Reduction using Multitemporal Filtering

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        filter : java.lang.String, ['None', 'Boxcar', 'Median', 'Frost', 'Gamma Map', 'Lee', 'Refined Lee', 'Lee Sigma', 'IDAN']
            Default 'Lee Sigma'
        filterSizeX : int
            The kernel x dimension
            Default '3'
        filterSizeY : int
            The kernel y dimension
            Default '3'
        dampingFactor : int
            The damping factor (Frost filter only)
            Default '2'
        estimateENL : boolean
            Default 'false'
        enl : double
            The number of looks
            Default '1.0'
        numLooksStr : java.lang.String, ['1', '2', '3', '4']
            Default '1'
        windowSize : java.lang.String, ['5x5', '7x7', '9x9', '11x11', '13x13', '15x15', '17x17']
            Default '7x7'
        targetWindowSizeStr : java.lang.String, ['3x3', '5x5']
            Default '3x3'
        sigmaStr : java.lang.String, ['0.5', '0.6', '0.7', '0.8', '0.9']
            Default '0.9'
        anSize : int
            The Adaptive Neighbourhood size
            Default '50'
        '''

        node = Node('Multi-Temporal-Speckle-Filter')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if filter:
            node.put('filter', filter)
        if filterSizeX:
            node.put('filterSizeX', filterSizeX)
        if filterSizeY:
            node.put('filterSizeY', filterSizeY)
        if dampingFactor:
            node.put('dampingFactor', dampingFactor)
        if estimateENL:
            node.put('estimateENL', estimateENL)
        if enl:
            node.put('enl', enl)
        if numLooksStr:
            node.put('numLooksStr', numLooksStr)
        if windowSize:
            node.put('windowSize', windowSize)
        if targetWindowSizeStr:
            node.put('targetWindowSizeStr', targetWindowSizeStr)
        if sigmaStr:
            node.put('sigmaStr', sigmaStr)
        if anSize:
            node.put('anSize', anSize)

        self.nodes.append(node)

    def add_cross_correlation(self,
        numGCPtoGenerate: int = None,
        coarseRegistrationWindowWidth = None,
        coarseRegistrationWindowHeight = None,
        rowInterpFactor = None,
        columnInterpFactor = None,
        maxIteration: int = None,
        gcpTolerance: float = None,
        applyFineRegistration: bool = None,
        inSAROptimized: bool = None,
        fineRegistrationWindowWidth = None,
        fineRegistrationWindowHeight = None,
        fineRegistrationWindowAccAzimuth = None,
        fineRegistrationWindowAccRange = None,
        fineRegistrationOversampling = None,
        coherenceWindowSize: int = None,
        coherenceThreshold: float = None,
        useSlidingWindow = None,
        computeOffset: bool = None,
        onlyGCPsOnLand: bool = None
        ):
        '''
        Automatic Selection of Ground Control Points

        Parameters
        ----------
        numGCPtoGenerate : int
            The number of GCPs to use in a grid
            Default '2000'
        coarseRegistrationWindowWidth : java.lang.String, ['32', '64', '128', '256', '512', '1024', '2048']
            Default '128'
        coarseRegistrationWindowHeight : java.lang.String, ['32', '64', '128', '256', '512', '1024', '2048']
            Default '128'
        rowInterpFactor : java.lang.String, ['2', '4', '8', '16']
            Default '2'
        columnInterpFactor : java.lang.String, ['2', '4', '8', '16']
            Default '2'
        maxIteration : int
            The maximum number of iterations
            Default '10'
        gcpTolerance : double
            Tolerance in slave GCP validation check
            Default '0.5'
        applyFineRegistration : boolean
            Default 'false'
        inSAROptimized : boolean
            Default 'false'
        fineRegistrationWindowWidth : java.lang.String, ['8', '16', '32', '64', '128', '256', '512']
            Default '32'
        fineRegistrationWindowHeight : java.lang.String, ['8', '16', '32', '64', '128', '256', '512']
            Default '32'
        fineRegistrationWindowAccAzimuth : java.lang.String, ['2', '4', '8', '16', '32', '64']
            Default '16'
        fineRegistrationWindowAccRange : java.lang.String, ['2', '4', '8', '16', '32', '64']
            Default '16'
        fineRegistrationOversampling : java.lang.String, ['2', '4', '8', '16', '32', '64']
            Default '16'
        coherenceWindowSize : int
            The coherence window size
            Default '3'
        coherenceThreshold : double
            The coherence threshold
            Default '0.6'
        useSlidingWindow : java.lang.Boolean
            Use sliding window for coherence calculation
            Default 'false'
        computeOffset : boolean
            Default 'false'
        onlyGCPsOnLand : boolean
            Default 'false'
        '''

        node = Node('Cross-Correlation')

        if numGCPtoGenerate:
            node.put('numGCPtoGenerate', numGCPtoGenerate)
        if coarseRegistrationWindowWidth:
            node.put('coarseRegistrationWindowWidth', coarseRegistrationWindowWidth)
        if coarseRegistrationWindowHeight:
            node.put('coarseRegistrationWindowHeight', coarseRegistrationWindowHeight)
        if rowInterpFactor:
            node.put('rowInterpFactor', rowInterpFactor)
        if columnInterpFactor:
            node.put('columnInterpFactor', columnInterpFactor)
        if maxIteration:
            node.put('maxIteration', maxIteration)
        if gcpTolerance:
            node.put('gcpTolerance', gcpTolerance)
        if applyFineRegistration:
            node.put('applyFineRegistration', applyFineRegistration)
        if inSAROptimized:
            node.put('inSAROptimized', inSAROptimized)
        if fineRegistrationWindowWidth:
            node.put('fineRegistrationWindowWidth', fineRegistrationWindowWidth)
        if fineRegistrationWindowHeight:
            node.put('fineRegistrationWindowHeight', fineRegistrationWindowHeight)
        if fineRegistrationWindowAccAzimuth:
            node.put('fineRegistrationWindowAccAzimuth', fineRegistrationWindowAccAzimuth)
        if fineRegistrationWindowAccRange:
            node.put('fineRegistrationWindowAccRange', fineRegistrationWindowAccRange)
        if fineRegistrationOversampling:
            node.put('fineRegistrationOversampling', fineRegistrationOversampling)
        if coherenceWindowSize:
            node.put('coherenceWindowSize', coherenceWindowSize)
        if coherenceThreshold:
            node.put('coherenceThreshold', coherenceThreshold)
        if useSlidingWindow:
            node.put('useSlidingWindow', useSlidingWindow)
        if computeOffset:
            node.put('computeOffset', computeOffset)
        if onlyGCPsOnLand:
            node.put('onlyGCPsOnLand', onlyGCPsOnLand)

        self.nodes.append(node)

    def add_meris_n1patcher(self,
        copyAllTiePoints: bool = None,
        patchedFile = None
        ):
        '''
        Copies an existing N1 file and replaces the data for the radiance bands

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        patchedFile : java.io.File
            The file to which the patched L1b product is written.
        '''

        node = Node('Meris.N1Patcher')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if patchedFile:
            node.put('patchedFile', patchedFile)

        self.nodes.append(node)

    def add_change_detection(self,
        sourceBandNames = None,
        maskUpperThreshold: float = None,
        maskLowerThreshold: float = None,
        includeSourceBands: bool = None,
        outputLogRatio: bool = None
        ):
        '''
        Change Detection.

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        maskUpperThreshold : float
            Mask upper threshold
            Default '2.0'
        maskLowerThreshold : float
            Mask lower threshold
            Default '-2.0'
        includeSourceBands : boolean
            Include source bands
            Default 'false'
        outputLogRatio : boolean
            Output Log Ratio
            Default 'false'
        '''

        node = Node('Change-Detection')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if maskUpperThreshold:
            node.put('maskUpperThreshold', maskUpperThreshold)
        if maskLowerThreshold:
            node.put('maskLowerThreshold', maskLowerThreshold)
        if includeSourceBands:
            node.put('includeSourceBands', includeSourceBands)
        if outputLogRatio:
            node.put('outputLogRatio', outputLogRatio)

        self.nodes.append(node)

    def add_multi_size_mosaic(self,
        variables = None,
        conditions = None,
        combine = None,
        crs = None,
        orthorectify: bool = None,
        elevationModelName = None,
        westBound: float = None,
        northBound: float = None,
        eastBound: float = None,
        southBound: float = None,
        pixelSizeX: float = None,
        pixelSizeY: float = None,
        resamplingName = None,
        nativeResolution: bool = None,
        overlappingMethod = None
        ):
        '''
        Creates a multi-size mosaic out of a set of source products.

        Parameters
        ----------
        variables : org.esa.snap.core.gpf.common.MosaicOp$Variable[]
            Specifies the bands in the target product.
        conditions : org.esa.snap.core.gpf.common.MosaicOp$Condition[]
            Specifies valid pixels considered in the target product.
        combine : java.lang.String, ['OR', 'AND']
            Specifies the way how conditions are combined.
            Default 'OR'
        crs : java.lang.String
            The CRS of the target product, represented as WKT or authority code.
            Default 'EPSG:4326'
        orthorectify : boolean
            Whether the source product should be orthorectified.
            Default 'false'
        elevationModelName : java.lang.String
            The name of the elevation model for the orthorectification.
        westBound : double
            The western longitude.
            Default '0'
        northBound : double
            The northern latitude.
            Default '0.1'
        eastBound : double
            The eastern longitude.
            Default '0.1'
        southBound : double
            The southern latitude.
            Default '0'
        pixelSizeX : double
            Size of a pixel in X-direction in map units.
            Default '0.005'
        pixelSizeY : double
            Size of a pixel in Y-direction in map units.
            Default '0.005'
        resamplingName : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for resampling.
            Default 'Nearest'
        nativeResolution : boolean
            Whether the resulting mosaic product should use the native resolutions of the source products.
            Default 'true'
        overlappingMethod : java.lang.String, ['MOSAIC_TYPE_BLEND', 'MOSAIC_TYPE_OVERLAY']
            The method used for overlapping pixels.
            Default 'MOSAIC_TYPE_OVERLAY'
        '''

        node = Node('Multi-size Mosaic')

        if variables:
            node.put('variables', variables)
        if conditions:
            node.put('conditions', conditions)
        if combine:
            node.put('combine', combine)
        if crs:
            node.put('crs', crs)
        if orthorectify:
            node.put('orthorectify', orthorectify)
        if elevationModelName:
            node.put('elevationModelName', elevationModelName)
        if westBound:
            node.put('westBound', westBound)
        if northBound:
            node.put('northBound', northBound)
        if eastBound:
            node.put('eastBound', eastBound)
        if southBound:
            node.put('southBound', southBound)
        if pixelSizeX:
            node.put('pixelSizeX', pixelSizeX)
        if pixelSizeY:
            node.put('pixelSizeY', pixelSizeY)
        if resamplingName:
            node.put('resamplingName', resamplingName)
        if nativeResolution:
            node.put('nativeResolution', nativeResolution)
        if overlappingMethod:
            node.put('overlappingMethod', overlappingMethod)

        self.nodes.append(node)

    def add_oversample(self,
        sourceBandNames = None,
        outputImageBy = None,
        targetImageHeight: int = None,
        targetImageWidth: int = None,
        widthRatio: float = None,
        heightRatio: float = None,
        rangeSpacing: float = None,
        azimuthSpacing: float = None,
        usePRFTileSize: bool = None
        ):
        '''
        Oversample the datset

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        outputImageBy : java.lang.String, ['Image Size', 'Ratio', 'Pixel Spacing']
            Default 'Ratio'
        targetImageHeight : int
            The row dimension of the output image
            Default '1000'
        targetImageWidth : int
            The col dimension of the output image
            Default '1000'
        widthRatio : float
            The width ratio of the output/input images
            Default '2.0'
        heightRatio : float
            The height ratio of the output/input images
            Default '2.0'
        rangeSpacing : float
            The range pixel spacing
            Default '12.5'
        azimuthSpacing : float
            The azimuth pixel spacing
            Default '12.5'
        usePRFTileSize : boolean
            use PRF as azimuth tile size and range line as range tile size
            Default 'false'
        '''

        node = Node('Oversample')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if outputImageBy:
            node.put('outputImageBy', outputImageBy)
        if targetImageHeight:
            node.put('targetImageHeight', targetImageHeight)
        if targetImageWidth:
            node.put('targetImageWidth', targetImageWidth)
        if widthRatio:
            node.put('widthRatio', widthRatio)
        if heightRatio:
            node.put('heightRatio', heightRatio)
        if rangeSpacing:
            node.put('rangeSpacing', rangeSpacing)
        if azimuthSpacing:
            node.put('azimuthSpacing', azimuthSpacing)
        if usePRFTileSize:
            node.put('usePRFTileSize', usePRFTileSize)

        self.nodes.append(node)

    def add_subset(self,
        bandNames = None,
        tiePointGridNames = None,
        region = None,
        referenceBand = None,
        geoRegion = None,
        subSamplingX: int = None,
        subSamplingY: int = None,
        fullSwath: bool = None,
        copyMetadata: bool = None
        ):
        '''
        Create a spatial and/or spectral subset of a data product.

        Parameters
        ----------
        bandNames : java.lang.String[]
            The list of source bands.
        tiePointGridNames : java.lang.String[]
            The list of tie-point grid names.
        region : java.awt.Rectangle
            The subset region in pixel coordinates.
            Use the following format: {x},{y},{width},{height}
            If not given, the entire scene is used. The 'geoRegion' parameter has precedence over this parameter.
        referenceBand : java.lang.String
            The band used to indicate the pixel coordinates.
        geoRegion : org.locationtech.jts.geom.Geometry
            The subset region in geographical coordinates using WKT-format,
            e.g. POLYGON(({lon1} {lat1}, {lon2} {lat2}, ..., {lon1} {lat1}))
            (make sure to quote the option due to spaces in {geometry}).
            If not given, the entire scene is used.
        subSamplingX : int
            The pixel sub-sampling step in X (horizontal image direction)
            Default '1'
        subSamplingY : int
            The pixel sub-sampling step in Y (vertical image direction)
            Default '1'
        fullSwath : boolean
            Forces the operator to extend the subset region to the full swath.
            Default 'false'
        copyMetadata : boolean
            Whether to copy the metadata of the source product.
            Default 'false'
        '''

        node = Node('Subset')

        if bandNames:
            node.put('bandNames', bandNames)
        if tiePointGridNames:
            node.put('tiePointGridNames', tiePointGridNames)
        if region:
            node.put('region', region)
        if referenceBand:
            node.put('referenceBand', referenceBand)
        if geoRegion:
            node.put('geoRegion', geoRegion)
        if subSamplingX:
            node.put('subSamplingX', subSamplingX)
        if subSamplingY:
            node.put('subSamplingY', subSamplingY)
        if fullSwath:
            node.put('fullSwath', fullSwath)
        if copyMetadata:
            node.put('copyMetadata', copyMetadata)

        self.nodes.append(node)

    def add_multitemporal_compositing(self
        ):
        '''
        Compute composite image from multi-temporal RTCs

        Parameters
        ----------
        '''

        node = Node('Multitemporal-Compositing')


        self.nodes.append(node)

    def add_test_pattern(self,
        sourceBandNames = None
        ):
        '''
        For testing only

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        '''

        node = Node('TestPattern')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)

        self.nodes.append(node)

    def add_kmeans_cluster_analysis(self,
        clusterCount: int = None,
        iterationCount: int = None,
        randomSeed: int = None,
        sourceBandNames = None,
        roiMaskName = None
        ):
        '''
        Performs a K-Means cluster analysis.

        Parameters
        ----------
        clusterCount : int
            Number of clusters
            Default '14'
        iterationCount : int
            Number of iterations
            Default '30'
        randomSeed : int
            Seed for the random generator, used for initialising the algorithm.
            Default '31415'
        sourceBandNames : java.lang.String[]
            The names of the bands being used for the cluster analysis.
        roiMaskName : java.lang.String
            The name of the ROI-Mask that should be used.
        '''

        node = Node('KMeansClusterAnalysis')

        if clusterCount:
            node.put('clusterCount', clusterCount)
        if iterationCount:
            node.put('iterationCount', iterationCount)
        if randomSeed:
            node.put('randomSeed', randomSeed)
        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if roiMaskName:
            node.put('roiMaskName', roiMaskName)

        self.nodes.append(node)

    def add_fu_classification(self,
        copyAllSourceBands: bool = None,
        inputIsIrradianceReflectance: bool = None,
        validExpression = None,
        reflectanceNamePattern = None,
        instrument = None,
        includeDominantLambda: bool = None,
        includeIntermediateResults: bool = None
        ):
        '''
        Colour classification based on the discrete Forel-Ule scale

        Parameters
        ----------
        copyAllSourceBands : boolean
            Weather or not to copy all the bands to the target product from the source product.
            Default 'false'
        inputIsIrradianceReflectance : boolean
            If enabled, the source reflectances will be converted to radiance reflectances by dividing it by PI before passing to the algorithm.
            Default 'false'
        validExpression : java.lang.String
            An expression to filter which pixel are considered.
        reflectanceNamePattern : java.lang.String
            The used reflectance band names must match the given pattern. Useful, if there is more then one spectrum in the product.
        instrument : org.esa.s3tbx.fu.Instrument
            The instrument to compute FU for.
            Default 'AUTO_DETECT'
        includeDominantLambda : boolean
            Whether or not the dominant wavelength shall be derived from the hue angle
            Default 'false'
        includeIntermediateResults : boolean
            Whether or not the intermediate results shall be written to the target output
            Default 'true'
        '''

        node = Node('FuClassification')

        if copyAllSourceBands:
            node.put('copyAllSourceBands', copyAllSourceBands)
        if inputIsIrradianceReflectance:
            node.put('inputIsIrradianceReflectance', inputIsIrradianceReflectance)
        if validExpression:
            node.put('validExpression', validExpression)
        if reflectanceNamePattern:
            node.put('reflectanceNamePattern', reflectanceNamePattern)
        if instrument:
            node.put('instrument', instrument)
        if includeDominantLambda:
            node.put('includeDominantLambda', includeDominantLambda)
        if includeIntermediateResults:
            node.put('includeIntermediateResults', includeIntermediateResults)

        self.nodes.append(node)

    def add_sarsim_terrain_correction(self,
        rmsThreshold: float = None,
        warpPolynomialOrder: int = None,
        imgResamplingMethod = None,
        pixelSpacingInMeter: float = None,
        pixelSpacingInDegree: float = None,
        mapProjection = None,
        alignToStandardGrid: bool = None,
        standardGridOriginX: float = None,
        standardGridOriginY: float = None,
        saveDEM: bool = None,
        saveLatLon: bool = None,
        saveLocalIncidenceAngle: bool = None,
        saveProjectedLocalIncidenceAngle: bool = None,
        saveSelectedSourceBand: bool = None,
        outputComplex: bool = None,
        applyRadiometricNormalization: bool = None,
        saveSigmaNought: bool = None,
        saveGammaNought: bool = None,
        saveBetaNought: bool = None,
        incidenceAngleForSigma0 = None,
        incidenceAngleForGamma0 = None,
        auxFile = None,
        externalAuxFile = None,
        openShiftsFile: bool = None,
        openResidualsFile: bool = None
        ):
        '''
        Orthorectification with SAR simulation

        Parameters
        ----------
        rmsThreshold : float
            The RMS threshold for eliminating invalid GCPs
            Default '1.0'
        warpPolynomialOrder : int, ['1', '2', '3']
            The order of WARP polynomial function
            Default '1'
        imgResamplingMethod : java.lang.String, ['NEAREST_NEIGHBOUR', 'BILINEAR_INTERPOLATION', 'CUBIC_CONVOLUTION']
            Default 'BILINEAR_INTERPOLATION'
        pixelSpacingInMeter : double
            The pixel spacing in meters
            Default '0'
        pixelSpacingInDegree : double
            The pixel spacing in degrees
            Default '0'
        mapProjection : java.lang.String
            The coordinate reference system in well known text format
        alignToStandardGrid : boolean
            Force the image grid to be aligned with a specific point
            Default 'false'
        standardGridOriginX : double
            x-coordinate of the standard grid's origin point
            Default '0'
        standardGridOriginY : double
            y-coordinate of the standard grid's origin point
            Default '0'
        saveDEM : boolean
            Default 'false'
        saveLatLon : boolean
            Default 'false'
        saveLocalIncidenceAngle : boolean
            Default 'false'
        saveProjectedLocalIncidenceAngle : boolean
            Default 'false'
        saveSelectedSourceBand : boolean
            Default 'true'
        outputComplex : boolean
            Default 'false'
        applyRadiometricNormalization : boolean
            Default 'false'
        saveSigmaNought : boolean
            Default 'false'
        saveGammaNought : boolean
            Default 'false'
        saveBetaNought : boolean
            Default 'false'
        incidenceAngleForSigma0 : java.lang.String, ['Use incidence angle from Ellipsoid', 'Use projected local incidence angle from DEM', 'Use local incidence angle from DEM']
            Default 'Use projected local incidence angle from DEM'
        incidenceAngleForGamma0 : java.lang.String, ['Use incidence angle from Ellipsoid', 'Use projected local incidence angle from DEM', 'Use local incidence angle from DEM']
            Default 'Use projected local incidence angle from DEM'
        auxFile : java.lang.String, ['Latest Auxiliary File', 'Product Auxiliary File', 'External Auxiliary File']
            The auxiliary file
            Default 'Latest Auxiliary File'
        externalAuxFile : java.io.File
            The antenne elevation pattern gain auxiliary data file.
        openShiftsFile : boolean
            Show range and azimuth shifts file in a text viewer
            Default 'false'
        openResidualsFile : boolean
            Show the Residuals file in a text viewer
            Default 'false'
        '''

        node = Node('SARSim-Terrain-Correction')

        if rmsThreshold:
            node.put('rmsThreshold', rmsThreshold)
        if warpPolynomialOrder:
            node.put('warpPolynomialOrder', warpPolynomialOrder)
        if imgResamplingMethod:
            node.put('imgResamplingMethod', imgResamplingMethod)
        if pixelSpacingInMeter:
            node.put('pixelSpacingInMeter', pixelSpacingInMeter)
        if pixelSpacingInDegree:
            node.put('pixelSpacingInDegree', pixelSpacingInDegree)
        if mapProjection:
            node.put('mapProjection', mapProjection)
        if alignToStandardGrid:
            node.put('alignToStandardGrid', alignToStandardGrid)
        if standardGridOriginX:
            node.put('standardGridOriginX', standardGridOriginX)
        if standardGridOriginY:
            node.put('standardGridOriginY', standardGridOriginY)
        if saveDEM:
            node.put('saveDEM', saveDEM)
        if saveLatLon:
            node.put('saveLatLon', saveLatLon)
        if saveLocalIncidenceAngle:
            node.put('saveLocalIncidenceAngle', saveLocalIncidenceAngle)
        if saveProjectedLocalIncidenceAngle:
            node.put('saveProjectedLocalIncidenceAngle', saveProjectedLocalIncidenceAngle)
        if saveSelectedSourceBand:
            node.put('saveSelectedSourceBand', saveSelectedSourceBand)
        if outputComplex:
            node.put('outputComplex', outputComplex)
        if applyRadiometricNormalization:
            node.put('applyRadiometricNormalization', applyRadiometricNormalization)
        if saveSigmaNought:
            node.put('saveSigmaNought', saveSigmaNought)
        if saveGammaNought:
            node.put('saveGammaNought', saveGammaNought)
        if saveBetaNought:
            node.put('saveBetaNought', saveBetaNought)
        if incidenceAngleForSigma0:
            node.put('incidenceAngleForSigma0', incidenceAngleForSigma0)
        if incidenceAngleForGamma0:
            node.put('incidenceAngleForGamma0', incidenceAngleForGamma0)
        if auxFile:
            node.put('auxFile', auxFile)
        if externalAuxFile:
            node.put('externalAuxFile', externalAuxFile)
        if openShiftsFile:
            node.put('openShiftsFile', openShiftsFile)
        if openResidualsFile:
            node.put('openResidualsFile', openResidualsFile)

        self.nodes.append(node)

    def add_owtclassification(self,
        owtType = None,
        reflectancesPrefix = None,
        inputReflectanceIs = None,
        writeInputReflectances: bool = None
        ):
        '''
        Performs an optical water type classification based on atmospherically corrected reflectances.

        Parameters
        ----------
        owtType : org.esa.s3tbx.owt.OWT_TYPE
            Default 'COASTAL'
        reflectancesPrefix : java.lang.String
            Default 'reflec'
        inputReflectanceIs : org.esa.s3tbx.owt.ReflectanceEnum
            Default 'RADIANCE_REFLECTANCES'
        writeInputReflectances : boolean
            Default 'false'
        '''

        node = Node('OWTClassification')

        if owtType:
            node.put('owtType', owtType)
        if reflectancesPrefix:
            node.put('reflectancesPrefix', reflectancesPrefix)
        if inputReflectanceIs:
            node.put('inputReflectanceIs', inputReflectanceIs)
        if writeInputReflectances:
            node.put('writeInputReflectances', writeInputReflectances)

        self.nodes.append(node)

    def add_more_then_an_integer_op(self
        ):
        '''
        just for testing

        Parameters
        ----------
        '''

        node = Node('MoreThenAnIntegerOp')


        self.nodes.append(node)

    def add_phase_to_elevation(self,
        demName = None,
        demResamplingMethod = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None
        ):
        '''
        DEM Generation

        Parameters
        ----------
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        demResamplingMethod : java.lang.String
            Default 'BILINEAR_INTERPOLATION'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        '''

        node = Node('PhaseToElevation')

        if demName:
            node.put('demName', demName)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)

        self.nodes.append(node)

    def add_integer_interferogram(self
        ):
        '''
        Create integer interferogram

        Parameters
        ----------
        '''

        node = Node('IntegerInterferogram')


        self.nodes.append(node)

    def add_rrto_frs(self
        ):
        '''
        None

        Parameters
        ----------
        '''

        node = Node('RRToFRS')


        self.nodes.append(node)

    def add_faraday_rotation_correction(self,
        windowSize: int = None
        ):
        '''
        Perform Faraday-rotation correction for quad-pol product

        Parameters
        ----------
        windowSize : int
            The sliding window size
            Default '10'
        '''

        node = Node('Faraday-Rotation-Correction')

        if windowSize:
            node.put('windowSize', windowSize)

        self.nodes.append(node)

    def add_meris_blue_band(self,
        copyAllTiePoints: bool = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        '''

        node = Node('Meris.BlueBand')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)

        self.nodes.append(node)

    def add_mph_chl_basis(self,
        validPixelExpression = None,
        cyanoMaxValue: float = None,
        chlThreshForFloatFlag: float = None,
        exportMph: bool = None
        ):
        '''
        Computes maximum peak height of chlorophyll. Basis class, contains sensor-independent parts.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Expression defining pixels considered for processing.
        cyanoMaxValue : double
            Maximum chlorophyll, arithmetically higher values are capped.
            Default '1000.0'
        chlThreshForFloatFlag : double
            Chlorophyll threshold, above which all cyanobacteria dominated waters are 'float.
            Default '350.0'
        exportMph : boolean
            Switch to true to write 'mph' band.
            Default 'false'
        '''

        node = Node('MphChlBasis')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if cyanoMaxValue:
            node.put('cyanoMaxValue', cyanoMaxValue)
        if chlThreshForFloatFlag:
            node.put('chlThreshForFloatFlag', chlThreshForFloatFlag)
        if exportMph:
            node.put('exportMph', exportMph)

        self.nodes.append(node)

    def add_pass_through(self
        ):
        '''
        Sets target product to source product.

        Parameters
        ----------
        '''

        node = Node('PassThrough')


        self.nodes.append(node)

    def add_data_analysis(self
        ):
        '''
        Computes statistics

        Parameters
        ----------
        '''

        node = Node('Data-Analysis')


        self.nodes.append(node)

    def add_land_cover_mask(self,
        sourceBandNames = None,
        landCoverBand = None,
        validLandCoverClasses = None,
        validPixelExpression = None,
        includeOtherBands: bool = None
        ):
        '''
        Perform decision tree classification

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        landCoverBand : java.lang.String
            Land cover band
        validLandCoverClasses : int[]
            Land cover classes to include
        validPixelExpression : java.lang.String
            Valid pixel expression
        includeOtherBands : boolean
            Add other bands unmasked
            Default 'false'
        '''

        node = Node('Land-Cover-Mask')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if landCoverBand:
            node.put('landCoverBand', landCoverBand)
        if validLandCoverClasses:
            node.put('validLandCoverClasses', validLandCoverClasses)
        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if includeOtherBands:
            node.put('includeOtherBands', includeOtherBands)

        self.nodes.append(node)

    def addc2rcc(self,
        sensorName = None,
        validPixelExpression = None,
        salinity: float = None,
        temperature: float = None,
        ozone: float = None,
        press: float = None,
        atmosphericAuxDataPath = None,
        outputRtosa: bool = None,
        useDefaultSolarFlux: bool = None,
        useEcmwfAuxData: bool = None,
        outputAsRrs: bool = None
        ):
        '''
        Performs atmospheric correction and IOP retrieval on OLCI, MSI, MERIS, MODIS or SeaWiFS L1 product.

        Parameters
        ----------
        sensorName : java.lang.String, ['', 'olci', 'msi', 'meris', 'meris4', 'modis', 'seawifs, viirs']
        validPixelExpression : java.lang.String
            If not specified a sensor specific default expression will be used.
        salinity : double
            The value used as salinity for the scene
            Default '35.0'
        temperature : double
            The value used as temperature for the scene
            Default '15.0'
        ozone : double
            The value used as ozone if not provided by auxiliary data
            Default '330'
        press : double
            The surface air pressure at sea level if not provided by auxiliary data
            Default '1000'
        atmosphericAuxDataPath : java.lang.String
            Path to the atmospheric auxiliary data directory. Use either this or the specific products. If the auxiliary data needed for interpolation is not available in this path, the data will automatically downloaded.
        outputRtosa : boolean
            Default 'false'
        useDefaultSolarFlux : boolean
            Default 'false'
        useEcmwfAuxData : boolean
            If selected, the ECMWF auxiliary data (ozone, air pressure) of the source product is used
            Default 'true'
        outputAsRrs : boolean
            Reflectance values in the target product shall be either written as remote sensing or water leaving reflectances
            Default 'false'
        '''

        node = Node('c2rcc')

        if sensorName:
            node.put('sensorName', sensorName)
        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if salinity:
            node.put('salinity', salinity)
        if temperature:
            node.put('temperature', temperature)
        if ozone:
            node.put('ozone', ozone)
        if press:
            node.put('press', press)
        if atmosphericAuxDataPath:
            node.put('atmosphericAuxDataPath', atmosphericAuxDataPath)
        if outputRtosa:
            node.put('outputRtosa', outputRtosa)
        if useDefaultSolarFlux:
            node.put('useDefaultSolarFlux', useDefaultSolarFlux)
        if useEcmwfAuxData:
            node.put('useEcmwfAuxData', useEcmwfAuxData)
        if outputAsRrs:
            node.put('outputAsRrs', outputAsRrs)

        self.nodes.append(node)

    def add_tndvi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        Transformed Normalized Difference Vegetation Index retrieves the Isovegetation lines parallel to soil line

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the TNDVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the TNDVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('TndviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_topsar_derampdemod(self,
        outputDerampDemodPhase: bool = None
        ):
        '''
        Bursts co-registration using orbit and DEM

        Parameters
        ----------
        outputDerampDemodPhase : boolean
            Default 'false'
        '''

        node = Node('TOPSAR-DerampDemod')

        if outputDerampDemodPhase:
            node.put('outputDerampDemodPhase', outputDerampDemodPhase)

        self.nodes.append(node)

    def add_smile_correction_olci(self
        ):
        '''
        Performs radiometric corrections on OLCI L1b data products.

        Parameters
        ----------
        '''

        node = Node('SmileCorrection.Olci')


        self.nodes.append(node)

    def addc2rcc_msi(self,
        validPixelExpression = None,
        salinity: float = None,
        temperature: float = None,
        ozone: float = None,
        press: float = None,
        elevation: float = None,
        TSMfakBpart: float = None,
        TSMfakBwit: float = None,
        CHLexp: float = None,
        CHLfak: float = None,
        thresholdRtosaOOS: float = None,
        thresholdAcReflecOos: float = None,
        thresholdCloudTDown865: float = None,
        atmosphericAuxDataPath = None,
        alternativeNNPath = None,
        netSet = None,
        outputAsRrs: bool = None,
        deriveRwFromPathAndTransmittance: bool = None,
        useEcmwfAuxData: bool = None,
        outputRtoa: bool = None,
        outputRtosaGc: bool = None,
        outputRtosaGcAann: bool = None,
        outputRpath: bool = None,
        outputTdown: bool = None,
        outputTup: bool = None,
        outputAcReflectance: bool = None,
        outputRhown: bool = None,
        outputOos: bool = None,
        outputKd: bool = None,
        outputUncertainties: bool = None
        ):
        '''
        Performs atmospheric correction and IOP retrieval with uncertainties on Sentinel-2 MSI L1C data products.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Defines the pixels which are valid for processing.
            Default 'B8 > 0 && B8 < 0.1'
        salinity : double
            The value used as salinity for the scene.
            Default '35.0'
        temperature : double
            The value used as temperature for the scene.
            Default '15.0'
        ozone : double
            The value used as ozone if not provided by auxiliary data.
            Default '330'
        press : double
            The surface air pressure at sea level if not provided by auxiliary data.
            Default '1000'
        elevation : double
            Used as fallback if elevation could not be taken from GETASSE30 DEM.
            Default '0'
        TSMfakBpart : double
            TSM factor (TSM = TSMfac * iop_btot^TSMexp).
            Default '1.06'
        TSMfakBwit : double
            TSM exponent (TSM = TSMfac * iop_btot^TSMexp).
            Default '0.942'
        CHLexp : double
            Chlorophyll exponent ( CHL = iop_apig^CHLexp * CHLfac).
            Default '1.04'
        CHLfak : double
            Chlorophyll factor ( CHL = iop_apig^CHLexp * CHLfac).
            Default '21.0'
        thresholdRtosaOOS : double
            Threshold for out of scope of nn training dataset flag for gas corrected top-of-atmosphere reflectances
            Default '0.05'
        thresholdAcReflecOos : double
            Threshold for out of scope of nn training dataset flag for atmospherically corrected reflectances
            Default '0.1'
        thresholdCloudTDown865 : double
            Threshold for cloud test based on downwelling transmittance @865
            Default '0.955'
        atmosphericAuxDataPath : java.lang.String
            Path to the atmospheric auxiliary data directory. Use either this or the specified products on the I/O Parameters tab. If the auxiliary data is not available at this path, the data will automatically be downloaded.
        alternativeNNPath : java.lang.String
            Path to an alternative set of neuronal nets. Use this to replace the standard set of neuronal nets.
        netSet : java.lang.String, ['C2RCC-Nets', 'C2X-Nets', 'C2X-COMPLEX-Nets']
            Set of neuronal nets for algorithm.
            Default 'C2RCC-Nets'
        outputAsRrs : boolean
            Write remote sensing reflectances instead of water leaving reflectances.
            Default 'false'
        deriveRwFromPathAndTransmittance : boolean
            Alternative way of calculating water reflectance. Still experimental.
            Default 'false'
        useEcmwfAuxData : boolean
            Use ECMWF auxiliary data (msl and tco3) from the source product, if available.
            Default 'false'
        outputRtoa : boolean
            Default 'true'
        outputRtosaGc : boolean
            Default 'false'
        outputRtosaGcAann : boolean
            Default 'false'
        outputRpath : boolean
            Default 'false'
        outputTdown : boolean
            Default 'false'
        outputTup : boolean
            Default 'false'
        outputAcReflectance : boolean
            Default 'true'
        outputRhown : boolean
            Default 'true'
        outputOos : boolean
            Default 'false'
        outputKd : boolean
            Default 'true'
        outputUncertainties : boolean
            Default 'true'
        '''

        node = Node('c2rcc.msi')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if salinity:
            node.put('salinity', salinity)
        if temperature:
            node.put('temperature', temperature)
        if ozone:
            node.put('ozone', ozone)
        if press:
            node.put('press', press)
        if elevation:
            node.put('elevation', elevation)
        if TSMfakBpart:
            node.put('TSMfakBpart', TSMfakBpart)
        if TSMfakBwit:
            node.put('TSMfakBwit', TSMfakBwit)
        if CHLexp:
            node.put('CHLexp', CHLexp)
        if CHLfak:
            node.put('CHLfak', CHLfak)
        if thresholdRtosaOOS:
            node.put('thresholdRtosaOOS', thresholdRtosaOOS)
        if thresholdAcReflecOos:
            node.put('thresholdAcReflecOos', thresholdAcReflecOos)
        if thresholdCloudTDown865:
            node.put('thresholdCloudTDown865', thresholdCloudTDown865)
        if atmosphericAuxDataPath:
            node.put('atmosphericAuxDataPath', atmosphericAuxDataPath)
        if alternativeNNPath:
            node.put('alternativeNNPath', alternativeNNPath)
        if netSet:
            node.put('netSet', netSet)
        if outputAsRrs:
            node.put('outputAsRrs', outputAsRrs)
        if deriveRwFromPathAndTransmittance:
            node.put('deriveRwFromPathAndTransmittance', deriveRwFromPathAndTransmittance)
        if useEcmwfAuxData:
            node.put('useEcmwfAuxData', useEcmwfAuxData)
        if outputRtoa:
            node.put('outputRtoa', outputRtoa)
        if outputRtosaGc:
            node.put('outputRtosaGc', outputRtosaGc)
        if outputRtosaGcAann:
            node.put('outputRtosaGcAann', outputRtosaGcAann)
        if outputRpath:
            node.put('outputRpath', outputRpath)
        if outputTdown:
            node.put('outputTdown', outputTdown)
        if outputTup:
            node.put('outputTup', outputTup)
        if outputAcReflectance:
            node.put('outputAcReflectance', outputAcReflectance)
        if outputRhown:
            node.put('outputRhown', outputRhown)
        if outputOos:
            node.put('outputOos', outputOos)
        if outputKd:
            node.put('outputKd', outputKd)
        if outputUncertainties:
            node.put('outputUncertainties', outputUncertainties)

        self.nodes.append(node)

    def add_smac_op(self,
        tauAero550 = None,
        uH2o = None,
        uO3 = None,
        surfPress = None,
        useMerisADS = None,
        aerosolType = None,
        invalidPixel = None,
        maskExpression = None,
        maskExpressionForward = None,
        bandNames = None
        ):
        '''
        Applies the Simplified Method for Atmospheric Corrections of Envisat MERIS/(A)ATSR measurements.

        Parameters
        ----------
        tauAero550 : java.lang.Float
            Aerosol optical depth
            Default '0.2'
        uH2o : java.lang.Float
            Relative humidity
            Default '3.0'
        uO3 : java.lang.Float
            Ozone content
            Default '0.15'
        surfPress : java.lang.Float
            Surface pressure
            Default '1013.0'
        useMerisADS : java.lang.Boolean
            Use ECMWF data in the MERIS ADS
            Default 'false'
        aerosolType : org.esa.s3tbx.smac.AEROSOL_TYPE
            Aerosol type
            Default 'CONTINENTAL'
        invalidPixel : java.lang.Float
            Default reflectance for invalid pixel
            Default '0.0'
        maskExpression : java.lang.String
            Mask expression for the whole view (MERIS) or the nadir view (AATSR)
        maskExpressionForward : java.lang.String
            Mask expression for the forward view (AATSR only)
        bandNames : java.lang.String[]
            Bands to process
        '''

        node = Node('SmacOp')

        if tauAero550:
            node.put('tauAero550', tauAero550)
        if uH2o:
            node.put('uH2o', uH2o)
        if uO3:
            node.put('uO3', uO3)
        if surfPress:
            node.put('surfPress', surfPress)
        if useMerisADS:
            node.put('useMerisADS', useMerisADS)
        if aerosolType:
            node.put('aerosolType', aerosolType)
        if invalidPixel:
            node.put('invalidPixel', invalidPixel)
        if maskExpression:
            node.put('maskExpression', maskExpression)
        if maskExpressionForward:
            node.put('maskExpressionForward', maskExpressionForward)
        if bandNames:
            node.put('bandNames', bandNames)

        self.nodes.append(node)

    def addc2rcc_landsat8(self,
        validPixelExpression = None,
        salinity: float = None,
        temperature: float = None,
        ozone: float = None,
        press: float = None,
        elevation: float = None,
        TSMfakBpart: float = None,
        TSMfakBwit: float = None,
        CHLexp: float = None,
        CHLfak: float = None,
        thresholdRtosaOOS: float = None,
        thresholdAcReflecOos: float = None,
        thresholdCloudTDown865: float = None,
        atmosphericAuxDataPath = None,
        alternativeNNPath = None,
        netSet = None,
        outputAsRrs: bool = None,
        deriveRwFromPathAndTransmittance: bool = None,
        outputRtoa: bool = None,
        outputRtosaGc: bool = None,
        outputRtosaGcAann: bool = None,
        outputRpath: bool = None,
        outputTdown: bool = None,
        outputTup: bool = None,
        outputAcReflectance: bool = None,
        outputRhown: bool = None,
        outputOos: bool = None,
        outputKd: bool = None,
        outputUncertainties: bool = None
        ):
        '''
        Performs atmospheric correction and IOP retrieval with uncertainties on Landsat-8 L1 data products.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Defines the pixels which are valid for processing.
        salinity : double
            The value used as salinity for the scene.
            Default '35.0'
        temperature : double
            The value used as temperature for the scene.
            Default '15.0'
        ozone : double
            The value used as ozone if not provided by auxiliary data.
            Default '330'
        press : double
            The surface air pressure at sea level if not provided by auxiliary data.
            Default '1000'
        elevation : double
            Used as fallback if elevation could not be taken from GETASSE30 DEM.
            Default '0'
        TSMfakBpart : double
            TSM factor (TSM = TSMfac * iop_btot^TSMexp).
            Default '1.72'
        TSMfakBwit : double
            TSM exponent (TSM = TSMfac * iop_btot^TSMexp).
            Default '3.1'
        CHLexp : double
            Chlorophyll exponent ( CHL = iop_apig^CHLexp * CHLfac).
            Default '1.04'
        CHLfak : double
            Chlorophyll factor ( CHL = iop_apig^CHLexp * CHLfac).
            Default '21.0'
        thresholdRtosaOOS : double
            Threshold for out of scope of nn training dataset flag for gas corrected top-of-atmosphere reflectances.
            Default '0.05'
        thresholdAcReflecOos : double
            Threshold for out of scope of nn training dataset flag for atmospherically corrected reflectances
            Default '0.1'
        thresholdCloudTDown865 : double
            Threshold for cloud test based on downwelling transmittance @865
            Default '0.955'
        atmosphericAuxDataPath : java.lang.String
            Path to the atmospheric auxiliary data directory. Use either this or the specified products on the I/O Parameters tab. If the auxiliary data is not available at this path, the data will automatically be downloaded.
        alternativeNNPath : java.lang.String
            Path to an alternative set of neuronal nets. Use this to replace the standard set of neuronal nets.
        netSet : java.lang.String, ['C2RCC-Nets', 'C2X-Nets']
            Set of neuronal nets for algorithm.
            Default 'C2RCC-Nets'
        outputAsRrs : boolean
            Write remote sensing reflectances instead of water leaving reflectances.
            Default 'false'
        deriveRwFromPathAndTransmittance : boolean
            Alternative way of calculating water reflectance. Still experimental.
            Default 'false'
        outputRtoa : boolean
            Default 'true'
        outputRtosaGc : boolean
            Default 'false'
        outputRtosaGcAann : boolean
            Default 'false'
        outputRpath : boolean
            Default 'false'
        outputTdown : boolean
            Default 'false'
        outputTup : boolean
            Default 'false'
        outputAcReflectance : boolean
            Default 'true'
        outputRhown : boolean
            Default 'true'
        outputOos : boolean
            Default 'false'
        outputKd : boolean
            Default 'true'
        outputUncertainties : boolean
            Default 'true'
        '''

        node = Node('c2rcc.landsat8')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if salinity:
            node.put('salinity', salinity)
        if temperature:
            node.put('temperature', temperature)
        if ozone:
            node.put('ozone', ozone)
        if press:
            node.put('press', press)
        if elevation:
            node.put('elevation', elevation)
        if TSMfakBpart:
            node.put('TSMfakBpart', TSMfakBpart)
        if TSMfakBwit:
            node.put('TSMfakBwit', TSMfakBwit)
        if CHLexp:
            node.put('CHLexp', CHLexp)
        if CHLfak:
            node.put('CHLfak', CHLfak)
        if thresholdRtosaOOS:
            node.put('thresholdRtosaOOS', thresholdRtosaOOS)
        if thresholdAcReflecOos:
            node.put('thresholdAcReflecOos', thresholdAcReflecOos)
        if thresholdCloudTDown865:
            node.put('thresholdCloudTDown865', thresholdCloudTDown865)
        if atmosphericAuxDataPath:
            node.put('atmosphericAuxDataPath', atmosphericAuxDataPath)
        if alternativeNNPath:
            node.put('alternativeNNPath', alternativeNNPath)
        if netSet:
            node.put('netSet', netSet)
        if outputAsRrs:
            node.put('outputAsRrs', outputAsRrs)
        if deriveRwFromPathAndTransmittance:
            node.put('deriveRwFromPathAndTransmittance', deriveRwFromPathAndTransmittance)
        if outputRtoa:
            node.put('outputRtoa', outputRtoa)
        if outputRtosaGc:
            node.put('outputRtosaGc', outputRtosaGc)
        if outputRtosaGcAann:
            node.put('outputRtosaGcAann', outputRtosaGcAann)
        if outputRpath:
            node.put('outputRpath', outputRpath)
        if outputTdown:
            node.put('outputTdown', outputTdown)
        if outputTup:
            node.put('outputTup', outputTup)
        if outputAcReflectance:
            node.put('outputAcReflectance', outputAcReflectance)
        if outputRhown:
            node.put('outputRhown', outputRhown)
        if outputOos:
            node.put('outputOos', outputOos)
        if outputKd:
            node.put('outputKd', outputKd)
        if outputUncertainties:
            node.put('outputUncertainties', outputUncertainties)

        self.nodes.append(node)

    def add_undersample(self,
        sourceBandNames = None,
        method = None,
        filterSize = None,
        subSamplingX: int = None,
        subSamplingY: int = None,
        outputImageBy = None,
        targetImageHeight: int = None,
        targetImageWidth: int = None,
        widthRatio: float = None,
        heightRatio: float = None,
        rangeSpacing: float = None,
        azimuthSpacing: float = None
        ):
        '''
        Undersample the datset

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        method : java.lang.String, ['Sub-Sampling', 'LowPass Filtering']
            Default 'LowPass Filtering'
        filterSize : java.lang.String, ['3x3', '5x5', '7x7']
            Default '3x3'
        subSamplingX : int
            Default '2'
        subSamplingY : int
            Default '2'
        outputImageBy : java.lang.String, ['Image Size', 'Ratio', 'Pixel Spacing']
            Default 'Ratio'
        targetImageHeight : int
            The row dimension of the output image
            Default '1000'
        targetImageWidth : int
            The col dimension of the output image
            Default '1000'
        widthRatio : float
            The width ratio of the output/input images
            Default '0.5'
        heightRatio : float
            The height ratio of the output/input images
            Default '0.5'
        rangeSpacing : float
            The range pixel spacing
            Default '12.5'
        azimuthSpacing : float
            The azimuth pixel spacing
            Default '12.5'
        '''

        node = Node('Undersample')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if method:
            node.put('method', method)
        if filterSize:
            node.put('filterSize', filterSize)
        if subSamplingX:
            node.put('subSamplingX', subSamplingX)
        if subSamplingY:
            node.put('subSamplingY', subSamplingY)
        if outputImageBy:
            node.put('outputImageBy', outputImageBy)
        if targetImageHeight:
            node.put('targetImageHeight', targetImageHeight)
        if targetImageWidth:
            node.put('targetImageWidth', targetImageWidth)
        if widthRatio:
            node.put('widthRatio', widthRatio)
        if heightRatio:
            node.put('heightRatio', heightRatio)
        if rangeSpacing:
            node.put('rangeSpacing', rangeSpacing)
        if azimuthSpacing:
            node.put('azimuthSpacing', azimuthSpacing)

        self.nodes.append(node)

    def add_gndvi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        greenFactor: float = None,
        nirFactor: float = None,
        greenSourceBand = None,
        nirSourceBand = None
        ):
        '''
        Green Normalized Difference Vegetation Index

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        greenFactor : float
            The value of the green source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        greenSourceBand : java.lang.String
            The green band for the GNDVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the GNDVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('GndviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if greenFactor:
            node.put('greenFactor', greenFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if greenSourceBand:
            node.put('greenSourceBand', greenSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_radar_vegetation_index(self,
        windowSize: int = None
        ):
        '''
        Dual-pol Radar Vegetation Indices generation

        Parameters
        ----------
        windowSize : int
            The sliding window size
            Default '5'
        '''

        node = Node('Radar-Vegetation-Index')

        if windowSize:
            node.put('windowSize', windowSize)

        self.nodes.append(node)

    def add_meris_gap_less_sdr(self,
        copyAllTiePoints: bool = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        '''

        node = Node('Meris.GapLessSdr')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)

        self.nodes.append(node)

    def add_mph_chl_meris(self,
        validPixelExpression = None,
        cyanoMaxValue: float = None,
        chlThreshForFloatFlag: float = None,
        exportMph: bool = None
        ):
        '''
        Computes maximum peak height of chlorophyll for MERIS. Implements MERIS-specific parts.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Expression defining pixels considered for processing.
        cyanoMaxValue : double
            Maximum chlorophyll, arithmetically higher values are capped.
            Default '1000.0'
        chlThreshForFloatFlag : double
            Chlorophyll threshold, above which all cyanobacteria dominated waters are 'float.
            Default '350.0'
        exportMph : boolean
            Switch to true to write 'mph' band.
            Default 'false'
        '''

        node = Node('MphChlMeris')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if cyanoMaxValue:
            node.put('cyanoMaxValue', cyanoMaxValue)
        if chlThreshForFloatFlag:
            node.put('chlThreshForFloatFlag', chlThreshForFloatFlag)
        if exportMph:
            node.put('exportMph', exportMph)

        self.nodes.append(node)

    def add_meris_rayleigh_correction(self,
        copyAllTiePoints: bool = None,
        correctWater: bool = None,
        exportRayCoeffs: bool = None,
        exportRhoR: bool = None
        ):
        '''
        MERIS L2 rayleigh correction.

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        correctWater : boolean
        exportRayCoeffs : boolean
        exportRhoR : boolean
        '''

        node = Node('Meris.RayleighCorrection')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if correctWater:
            node.put('correctWater', correctWater)
        if exportRayCoeffs:
            node.put('exportRayCoeffs', exportRayCoeffs)
        if exportRhoR:
            node.put('exportRhoR', exportRhoR)

        self.nodes.append(node)

    def add_spectral_angle_mapper_op(self,
        referenceBands = None,
        thresholds = None,
        spectra = None,
        hiddenSpectra = None,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None
        ):
        '''
        Classifies a product using the spectral angle mapper algorithm

        Parameters
        ----------
        referenceBands : java.lang.String[]
            The reference bands to be used for the Spectral Angle Mapper Processor 
        thresholds : java.lang.String
            thresholds
            Default '0.0'
        spectra : org.esa.s2tbx.mapper.common.SpectrumInput[]
            The list of spectra.
        hiddenSpectra : org.esa.s2tbx.mapper.common.SpectrumInput[]
            The list of spectra.
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected bands differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        '''

        node = Node('SpectralAngleMapperOp')

        if referenceBands:
            node.put('referenceBands', referenceBands)
        if thresholds:
            node.put('thresholds', thresholds)
        if spectra:
            node.put('spectra', spectra)
        if hiddenSpectra:
            node.put('hiddenSpectra', hiddenSpectra)
        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)

        self.nodes.append(node)

    def add_adaptive_thresholding(self,
        targetWindowSizeInMeter: int = None,
        guardWindowSizeInMeter: float = None,
        backgroundWindowSizeInMeter: float = None,
        pfa: float = None,
        estimateBackground = None
        ):
        '''
        Detect ships using Constant False Alarm Rate detector.

        Parameters
        ----------
        targetWindowSizeInMeter : int
            Target window size
            Default '50'
        guardWindowSizeInMeter : double
            Guard window size
            Default '500.0'
        backgroundWindowSizeInMeter : double
            Background window size
            Default '800.0'
        pfa : double
            Probability of false alarm
            Default '6.5'
        estimateBackground : java.lang.Boolean
            Rough estimation of background threshold for quicker processing
            Default 'false'
        '''

        node = Node('AdaptiveThresholding')

        if targetWindowSizeInMeter:
            node.put('targetWindowSizeInMeter', targetWindowSizeInMeter)
        if guardWindowSizeInMeter:
            node.put('guardWindowSizeInMeter', guardWindowSizeInMeter)
        if backgroundWindowSizeInMeter:
            node.put('backgroundWindowSizeInMeter', backgroundWindowSizeInMeter)
        if pfa:
            node.put('pfa', pfa)
        if estimateBackground:
            node.put('estimateBackground', estimateBackground)

        self.nodes.append(node)

    def add_horizontal_vertical_motion(self,
        refPixelX: int = None,
        refPixelY: int = None
        ):
        '''
        Computation of Horizontal/Vertical Motion Components

        Parameters
        ----------
        refPixelX : int
            X position for reference pixel
            Default '0'
        refPixelY : int
            Y position for reference pixel
            Default '0'
        '''

        node = Node('HorizontalVerticalMotion')

        if refPixelX:
            node.put('refPixelX', refPixelX)
        if refPixelY:
            node.put('refPixelY', refPixelY)

        self.nodes.append(node)

    def addc2rcc_olci(self,
        validPixelExpression = None,
        salinity: float = None,
        temperature: float = None,
        ozone: float = None,
        press: float = None,
        TSMfakBpart: float = None,
        TSMfakBwit: float = None,
        CHLexp: float = None,
        CHLfak: float = None,
        thresholdRtosaOOS: float = None,
        thresholdAcReflecOos: float = None,
        thresholdCloudTDown865: float = None,
        atmosphericAuxDataPath = None,
        alternativeNNPath = None,
        outputAsRrs: bool = None,
        deriveRwFromPathAndTransmittance: bool = None,
        useEcmwfAuxData: bool = None,
        outputRtoa: bool = None,
        outputRtosaGc: bool = None,
        outputRtosaGcAann: bool = None,
        outputRpath: bool = None,
        outputTdown: bool = None,
        outputTup: bool = None,
        outputAcReflectance: bool = None,
        outputRhown: bool = None,
        outputOos: bool = None,
        outputKd: bool = None,
        outputUncertainties: bool = None
        ):
        '''
        Performs atmospheric correction and IOP retrieval with uncertainties on SENTINEL-3 OLCI L1B data products.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Defines the pixels which are valid for processing.
            Default '!quality_flags.invalid && (!quality_flags.land || quality_flags.fresh_inland_water)'
        salinity : double
            The value used as salinity for the scene.
            Default '35.0'
        temperature : double
            The value used as temperature for the scene.
            Default '15.0'
        ozone : double
            The value used as ozone if not provided by auxiliary data.
            Default '330'
        press : double
            The surface air pressure at sea level if not provided by auxiliary data.
            Default '1000'
        TSMfakBpart : double
            TSM factor (TSM = TSMfac * iop_btot^TSMexp).
            Default '1.06'
        TSMfakBwit : double
            TSM exponent (TSM = TSMfac * iop_btot^TSMexp).
            Default '0.942'
        CHLexp : double
            Chlorophyll exponent ( CHL = iop_apig^CHLexp * CHLfac).
            Default '1.04'
        CHLfak : double
            Chlorophyll factor ( CHL = iop_apig^CHLexp * CHLfac).
            Default '21.0'
        thresholdRtosaOOS : double
            Threshold for nn training dataset out of scope flag for gas corrected top-of-atmosphere reflectances.
            Default '0.01'
        thresholdAcReflecOos : double
            Threshold for nn training dataset out of scope flag for atmospherically corrected reflectances.
            Default '0.15'
        thresholdCloudTDown865 : double
            Threshold for cloud test based on downwelling transmittance @865.
            Default '0.955'
        atmosphericAuxDataPath : java.lang.String
            Path to the atmospheric auxiliary data directory. Use either this or the specified products on the I/O Parameters tab. If the auxiliary data is not available at this path, the data will automatically be downloaded.
        alternativeNNPath : java.lang.String
            Path to an alternative set of neuronal nets. Use this to replace the standard set of neuronal nets.
        outputAsRrs : boolean
            Write remote sensing reflectances instead of water leaving reflectances.
            Default 'false'
        deriveRwFromPathAndTransmittance : boolean
            Alternative way of calculating water reflectance. Still experimental.
            Default 'false'
        useEcmwfAuxData : boolean
            Use ECMWF auxiliary data (total_ozone, sea_level_pressure) from the source product.
            Default 'true'
        outputRtoa : boolean
            Default 'true'
        outputRtosaGc : boolean
            Default 'false'
        outputRtosaGcAann : boolean
            Default 'false'
        outputRpath : boolean
            Default 'false'
        outputTdown : boolean
            Default 'false'
        outputTup : boolean
            Default 'false'
        outputAcReflectance : boolean
            Default 'true'
        outputRhown : boolean
            Default 'true'
        outputOos : boolean
            Default 'false'
        outputKd : boolean
            Default 'true'
        outputUncertainties : boolean
            Default 'true'
        '''

        node = Node('c2rcc.olci')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if salinity:
            node.put('salinity', salinity)
        if temperature:
            node.put('temperature', temperature)
        if ozone:
            node.put('ozone', ozone)
        if press:
            node.put('press', press)
        if TSMfakBpart:
            node.put('TSMfakBpart', TSMfakBpart)
        if TSMfakBwit:
            node.put('TSMfakBwit', TSMfakBwit)
        if CHLexp:
            node.put('CHLexp', CHLexp)
        if CHLfak:
            node.put('CHLfak', CHLfak)
        if thresholdRtosaOOS:
            node.put('thresholdRtosaOOS', thresholdRtosaOOS)
        if thresholdAcReflecOos:
            node.put('thresholdAcReflecOos', thresholdAcReflecOos)
        if thresholdCloudTDown865:
            node.put('thresholdCloudTDown865', thresholdCloudTDown865)
        if atmosphericAuxDataPath:
            node.put('atmosphericAuxDataPath', atmosphericAuxDataPath)
        if alternativeNNPath:
            node.put('alternativeNNPath', alternativeNNPath)
        if outputAsRrs:
            node.put('outputAsRrs', outputAsRrs)
        if deriveRwFromPathAndTransmittance:
            node.put('deriveRwFromPathAndTransmittance', deriveRwFromPathAndTransmittance)
        if useEcmwfAuxData:
            node.put('useEcmwfAuxData', useEcmwfAuxData)
        if outputRtoa:
            node.put('outputRtoa', outputRtoa)
        if outputRtosaGc:
            node.put('outputRtosaGc', outputRtosaGc)
        if outputRtosaGcAann:
            node.put('outputRtosaGcAann', outputRtosaGcAann)
        if outputRpath:
            node.put('outputRpath', outputRpath)
        if outputTdown:
            node.put('outputTdown', outputTdown)
        if outputTup:
            node.put('outputTup', outputTup)
        if outputAcReflectance:
            node.put('outputAcReflectance', outputAcReflectance)
        if outputRhown:
            node.put('outputRhown', outputRhown)
        if outputOos:
            node.put('outputOos', outputOos)
        if outputKd:
            node.put('outputKd', outputKd)
        if outputUncertainties:
            node.put('outputUncertainties', outputUncertainties)

        self.nodes.append(node)

    def add_mcari_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        red1Factor: float = None,
        red2Factor: float = None,
        greenFactor: float = None,
        red1SourceBand = None,
        red2SourceBand = None,
        greenSourceBand = None
        ):
        '''
        Modified Chlorophyll Absorption Ratio Index, developed to be responsive to chlorophyll variation

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        red1Factor : float
            The value of the red source band (B4) is multiplied by this value.
            Default '1.0F'
        red2Factor : float
            The value of the red source band (B5) is multiplied by this value.
            Default '1.0F'
        greenFactor : float
            The value of the green source band is multiplied by this value.
            Default '1.0F'
        red1SourceBand : java.lang.String
            The first red band for the MCARI computation. Choose B4 for Sentinel-2. If not provided, the operator will try to find the best fitting band.
        red2SourceBand : java.lang.String
            The second red band for the MCARI computation. Choose B5 for Sentinel-2. If not provided, the operator will try to find the best fitting band.
        greenSourceBand : java.lang.String
            The green band for the MCARI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('McariOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if red1Factor:
            node.put('red1Factor', red1Factor)
        if red2Factor:
            node.put('red2Factor', red2Factor)
        if greenFactor:
            node.put('greenFactor', greenFactor)
        if red1SourceBand:
            node.put('red1SourceBand', red1SourceBand)
        if red2SourceBand:
            node.put('red2SourceBand', red2SourceBand)
        if greenSourceBand:
            node.put('greenSourceBand', greenSourceBand)

        self.nodes.append(node)

    def add_sar_simulation(self,
        sourceBandNames = None,
        demName = None,
        demResamplingMethod = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        externalDEMApplyEGM = None,
        saveLayoverShadowMask: bool = None
        ):
        '''
        Rigorous SAR Simulation

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        demResamplingMethod : java.lang.String
            Default 'BICUBIC_INTERPOLATION'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        externalDEMApplyEGM : java.lang.Boolean
            Default 'true'
        saveLayoverShadowMask : boolean
            Default 'false'
        '''

        node = Node('SAR-Simulation')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if demName:
            node.put('demName', demName)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if externalDEMApplyEGM:
            node.put('externalDEMApplyEGM', externalDEMApplyEGM)
        if saveLayoverShadowMask:
            node.put('saveLayoverShadowMask', saveLayoverShadowMask)

        self.nodes.append(node)

    def add_terrain_mask(self,
        demName = None,
        demResamplingMethod = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        windowSizeStr = None,
        thresholdInMeter: float = None
        ):
        '''
        Terrain Mask Generation

        Parameters
        ----------
        demName : java.lang.String, ['ACE', 'ASTER 1sec GDEM', 'GETASSE30', 'SRTM 1Sec HGT', 'SRTM 3Sec']
            The digital elevation model.
            Default 'SRTM 3Sec'
        demResamplingMethod : java.lang.String, ['NEAREST_NEIGHBOUR', 'BILINEAR_INTERPOLATION', 'CUBIC_CONVOLUTION', 'BICUBIC_INTERPOLATION', 'BISINC_5_POINT_INTERPOLATION']
            Default 'NEAREST_NEIGHBOUR'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        windowSizeStr : java.lang.String, ['5x5', '7x7', '9x9', '11x11', '13x13', '15x15', '17x17']
            Default '15x15'
        thresholdInMeter : double
            Threshold for detection
            Default '40.0'
        '''

        node = Node('Terrain-Mask')

        if demName:
            node.put('demName', demName)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if windowSizeStr:
            node.put('windowSizeStr', windowSizeStr)
        if thresholdInMeter:
            node.put('thresholdInMeter', thresholdInMeter)

        self.nodes.append(node)

    def add_warp(self,
        rmsThreshold: float = None,
        warpPolynomialOrder: int = None,
        interpolationMethod = None,
        demRefinement = None,
        demName = None,
        excludeMaster: bool = None,
        openResidualsFile = None
        ):
        '''
        Create Warp Function And Get Co-registrated Images

        Parameters
        ----------
        rmsThreshold : float, ['0.001', '0.05', '0.1', '0.5', '1.0']
            Confidence level for outlier detection procedure, lower value accepts more outliers
            Default '0.05'
        warpPolynomialOrder : int, ['1', '2', '3']
            The order of WARP polynomial function
            Default '2'
        interpolationMethod : java.lang.String, ['Nearest-neighbor interpolation', 'Bilinear interpolation', 'Bicubic interpolation', 'Bicubic2 interpolation', 'Linear interpolation', 'Cubic convolution (4 points)', 'Cubic convolution (6 points)', 'Truncated sinc (6 points)', 'Truncated sinc (8 points)', 'Truncated sinc (16 points)']
            Default 'Cubic convolution (6 points)'
        demRefinement : java.lang.Boolean
            Refine estimated offsets using a-priori DEM
            Default 'false'
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        excludeMaster : boolean
            Default 'false'
        openResidualsFile : java.lang.Boolean
            Show the Residuals file in a text viewer
            Default 'false'
        '''

        node = Node('Warp')

        if rmsThreshold:
            node.put('rmsThreshold', rmsThreshold)
        if warpPolynomialOrder:
            node.put('warpPolynomialOrder', warpPolynomialOrder)
        if interpolationMethod:
            node.put('interpolationMethod', interpolationMethod)
        if demRefinement:
            node.put('demRefinement', demRefinement)
        if demName:
            node.put('demName', demName)
        if excludeMaster:
            node.put('excludeMaster', excludeMaster)
        if openResidualsFile:
            node.put('openResidualsFile', openResidualsFile)

        self.nodes.append(node)

    def add_kdtree_knn_classifier(self,
        numNeighbours: int = None,
        numTrainSamples: int = None,
        savedClassifierName = None,
        doLoadClassifier = None,
        doClassValQuantization = None,
        minClassValue = None,
        classValStepSize = None,
        classLevels: int = None,
        trainOnRaster = None,
        trainingBands = None,
        trainingVectors = None,
        featureBands = None,
        labelSource = None,
        evaluateClassifier = None,
        evaluateFeaturePowerSet = None,
        minPowerSetSize = None,
        maxPowerSetSize = None
        ):
        '''
        KDTree KNN classifier

        Parameters
        ----------
        numNeighbours : int
            The number of neighbours
            Default '5'
        numTrainSamples : int
            The number of training samples
            Default '5000'
        savedClassifierName : java.lang.String
            The saved classifier name
        doLoadClassifier : java.lang.Boolean
            Choose to save or load classifier
            Default 'false'
        doClassValQuantization : java.lang.Boolean
            Quantization for raster traiing
            Default 'true'
        minClassValue : java.lang.Double
            Quantization min class value for raster traiing
            Default '0.0'
        classValStepSize : java.lang.Double
            Quantization step size for raster traiing
            Default '5.0'
        classLevels : int
            Quantization class levels for raster traiing
            Default '101'
        trainOnRaster : java.lang.Boolean
            Train on raster or vector data
            Default 'true'
        trainingBands : java.lang.String[]
            Raster bands to train on
        trainingVectors : java.lang.String[]
            Vectors to train on
        featureBands : java.lang.String[]
            Names of bands to be used as features
        labelSource : java.lang.String
            'VectorNodeName' or specific Attribute name
        evaluateClassifier : java.lang.Boolean
            Evaluate classifier and features
        evaluateFeaturePowerSet : java.lang.Boolean
            Evaluate the power set of features
            Default 'false'
        minPowerSetSize : java.lang.Integer
            Minimum size of the power set of features
            Default '2'
        maxPowerSetSize : java.lang.Integer
            Maximum size of the power set of features
            Default '7'
        '''

        node = Node('KDTree-KNN-Classifier')

        if numNeighbours:
            node.put('numNeighbours', numNeighbours)
        if numTrainSamples:
            node.put('numTrainSamples', numTrainSamples)
        if savedClassifierName:
            node.put('savedClassifierName', savedClassifierName)
        if doLoadClassifier:
            node.put('doLoadClassifier', doLoadClassifier)
        if doClassValQuantization:
            node.put('doClassValQuantization', doClassValQuantization)
        if minClassValue:
            node.put('minClassValue', minClassValue)
        if classValStepSize:
            node.put('classValStepSize', classValStepSize)
        if classLevels:
            node.put('classLevels', classLevels)
        if trainOnRaster:
            node.put('trainOnRaster', trainOnRaster)
        if trainingBands:
            node.put('trainingBands', trainingBands)
        if trainingVectors:
            node.put('trainingVectors', trainingVectors)
        if featureBands:
            node.put('featureBands', featureBands)
        if labelSource:
            node.put('labelSource', labelSource)
        if evaluateClassifier:
            node.put('evaluateClassifier', evaluateClassifier)
        if evaluateFeaturePowerSet:
            node.put('evaluateFeaturePowerSet', evaluateFeaturePowerSet)
        if minPowerSetSize:
            node.put('minPowerSetSize', minPowerSetSize)
        if maxPowerSetSize:
            node.put('maxPowerSetSize', maxPowerSetSize)

        self.nodes.append(node)

    def add_tile_writer(self,
        file = None,
        formatName = None,
        divisionBy = None,
        numberOfTiles = None,
        pixelSizeX: int = None,
        pixelSizeY: int = None,
        overlap: int = None
        ):
        '''
        Writes a data product to a tiles.

        Parameters
        ----------
        file : java.io.File
            The output file to which the data product is written.
        formatName : java.lang.String
            The name of the output file format.
            Default 'BEAM-DIMAP'
        divisionBy : java.lang.String, ['Tiles', 'Pixels']
            How to divide the tiles
            Default 'Tiles'
        numberOfTiles : java.lang.String, ['2', '4', '9', '16', '36', '64', '100', '256']
            The number of output tiles
            Default '4'
        pixelSizeX : int
            Tile pixel width
            Default '200'
        pixelSizeY : int
            Tile pixel height
            Default '200'
        overlap : int
            Tile overlap
            Default '0'
        '''

        node = Node('TileWriter')

        if file:
            node.put('file', file)
        if formatName:
            node.put('formatName', formatName)
        if divisionBy:
            node.put('divisionBy', divisionBy)
        if numberOfTiles:
            node.put('numberOfTiles', numberOfTiles)
        if pixelSizeX:
            node.put('pixelSizeX', pixelSizeX)
        if pixelSizeY:
            node.put('pixelSizeY', pixelSizeY)
        if overlap:
            node.put('overlap', overlap)

        self.nodes.append(node)

    def add_srgr(self,
        sourceBandNames = None,
        warpPolynomialOrder: int = None,
        interpolationMethod = None
        ):
        '''
        Converts Slant Range to Ground Range

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        warpPolynomialOrder : int, ['1', '2', '3', '4']
            The order of WARP polynomial function
            Default '4'
        interpolationMethod : java.lang.String, ['Nearest-neighbor interpolation', 'Linear interpolation', 'Cubic interpolation', 'Cubic2 interpolation', 'Sinc interpolation']
            Default 'Linear interpolation'
        '''

        node = Node('SRGR')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if warpPolynomialOrder:
            node.put('warpPolynomialOrder', warpPolynomialOrder)
        if interpolationMethod:
            node.put('interpolationMethod', interpolationMethod)

        self.nodes.append(node)

    def add_msavi2_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        This retrieves the second Modified Soil Adjusted Vegetation Index (MSAVI2).

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the RED source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the MSAVI2 computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the MSAVI2 computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('Msavi2Op')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_biophysical10m_op(self,
        sensor = None,
        computeLAI: bool = None,
        computeFapar: bool = None,
        computeFcover: bool = None
        ):
        '''
        The 'Biophysical Processor' operator retrieves LAI from atmospherically corrected Sentinel-2 products

        Parameters
        ----------
        sensor : java.lang.String, ['S2A_10m', 'S2B_10m']
            Sensor
            Default 'S2A_10m'
        computeLAI : boolean
            Compute LAI (Leaf Area Index)
            Default 'true'
        computeFapar : boolean
            Compute FAPAR (Fraction of Absorbed Photosynthetically Active Radiation)
            Default 'true'
        computeFcover : boolean
            Compute FVC (Fraction of Vegetation Cover)
            Default 'true'
        '''

        node = Node('Biophysical10mOp')

        if sensor:
            node.put('sensor', sensor)
        if computeLAI:
            node.put('computeLAI', computeLAI)
        if computeFapar:
            node.put('computeFapar', computeFapar)
        if computeFcover:
            node.put('computeFcover', computeFcover)

        self.nodes.append(node)

    def add_coherence(self,
        cohWinAz: int = None,
        cohWinRg: int = None,
        subtractFlatEarthPhase: bool = None,
        srpPolynomialDegree: int = None,
        srpNumberPoints: int = None,
        orbitDegree: int = None,
        squarePixel = None,
        subtractTopographicPhase: bool = None,
        demName = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        externalDEMApplyEGM = None,
        tileExtensionPercent = None,
        singleMaster = None
        ):
        '''
        Estimate coherence from stack of coregistered images

        Parameters
        ----------
        cohWinAz : int
            Size of coherence estimation window in Azimuth direction
            Default '10'
        cohWinRg : int
            Size of coherence estimation window in Range direction
            Default '10'
        subtractFlatEarthPhase : boolean
            Default 'false'
        srpPolynomialDegree : int, ['1', '2', '3', '4', '5', '6', '7', '8']
            Order of 'Flat earth phase' polynomial
            Default '5'
        srpNumberPoints : int, ['301', '401', '501', '601', '701', '801', '901', '1001']
            Number of points for the 'flat earth phase' polynomial estimation
            Default '501'
        orbitDegree : int, ['1', '2', '3', '4', '5']
            Degree of orbit (polynomial) interpolator
            Default '3'
        squarePixel : java.lang.Boolean
            Use ground square pixel
            Default 'true'
        subtractTopographicPhase : boolean
            Default 'false'
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        externalDEMApplyEGM : java.lang.Boolean
            Default 'true'
        tileExtensionPercent : java.lang.String
            Define extension of tile for DEM simulation (optimization parameter).
            Default '100'
        singleMaster : java.lang.Boolean
            Default 'true'
        '''

        node = Node('Coherence')

        if cohWinAz:
            node.put('cohWinAz', cohWinAz)
        if cohWinRg:
            node.put('cohWinRg', cohWinRg)
        if subtractFlatEarthPhase:
            node.put('subtractFlatEarthPhase', subtractFlatEarthPhase)
        if srpPolynomialDegree:
            node.put('srpPolynomialDegree', srpPolynomialDegree)
        if srpNumberPoints:
            node.put('srpNumberPoints', srpNumberPoints)
        if orbitDegree:
            node.put('orbitDegree', orbitDegree)
        if squarePixel:
            node.put('squarePixel', squarePixel)
        if subtractTopographicPhase:
            node.put('subtractTopographicPhase', subtractTopographicPhase)
        if demName:
            node.put('demName', demName)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if externalDEMApplyEGM:
            node.put('externalDEMApplyEGM', externalDEMApplyEGM)
        if tileExtensionPercent:
            node.put('tileExtensionPercent', tileExtensionPercent)
        if singleMaster:
            node.put('singleMaster', singleMaster)

        self.nodes.append(node)

    def add_fub_water(self,
        computeCHL: bool = None,
        computeYS: bool = None,
        computeTSM: bool = None,
        computeAtmCorr: bool = None,
        checkWhetherSuspectIsValid: bool = None,
        expression = None
        ):
        '''
        MERIS FUB-CSIRO Coastal Water Processor to retrieve case II water properties and atmospheric properties

        Parameters
        ----------
        computeCHL : boolean
            Whether chlorophyll-a concentration band shall be computed
            Default 'true'
        computeYS : boolean
            Whether yellow substances band shall be computed
            Default 'true'
        computeTSM : boolean
            Whether total suspended matter band shall be computed
            Default 'true'
        computeAtmCorr : boolean
            Whether atmospheric correction bands shall be computed
            Default 'true'
        checkWhetherSuspectIsValid : boolean
            Expert parameter. Performs a check whether the 'l1_flags.SUSPECT' shall be considered in an expression.This parameter is only considered when the expression contains the term 'and not l1_flags.SUSPECT'
            Default 'true'
        expression : java.lang.String
            Band maths expression which defines valid pixels. If the expression is empty,all pixels will be considered.
            Default 'not l1_flags.GLINT_RISK and not l1_flags.BRIGHT and not l1_flags.INVALID and not l1_flags.SUSPECT'
        '''

        node = Node('FUB.Water')

        if computeCHL:
            node.put('computeCHL', computeCHL)
        if computeYS:
            node.put('computeYS', computeYS)
        if computeTSM:
            node.put('computeTSM', computeTSM)
        if computeAtmCorr:
            node.put('computeAtmCorr', computeAtmCorr)
        if checkWhetherSuspectIsValid:
            node.put('checkWhetherSuspectIsValid', checkWhetherSuspectIsValid)
        if expression:
            node.put('expression', expression)

        self.nodes.append(node)

    def add_iem_multi_pol_inversion(self,
        N = None,
        M = None,
        doRemainingOutliersFilter = None,
        lutFile = None,
        outputRMS = None,
        thresholdRDC = None
        ):
        '''
        Performs IEM inversion using Multi-polarization approach

        Parameters
        ----------
        N : java.lang.Integer
            # closest sigma match from LUT search
            Default '5'
        M : java.lang.Integer
            Length (pixels) of side of square neighbourhood (M)
            Default '5'
        doRemainingOutliersFilter : java.lang.Boolean
            Replace remaining outlier with neighbours's average
            Default 'true'
        lutFile : java.io.File
        outputRMS : java.lang.Boolean
            Optional rms in output
            Default 'false'
        thresholdRDC : java.lang.Double
            RDC deviation threshold
            Default '0.5'
        '''

        node = Node('IEM-Multi-Pol-Inversion')

        if N:
            node.put('N', N)
        if M:
            node.put('M', M)
        if doRemainingOutliersFilter:
            node.put('doRemainingOutliersFilter', doRemainingOutliersFilter)
        if lutFile:
            node.put('lutFile', lutFile)
        if outputRMS:
            node.put('outputRMS', outputRMS)
        if thresholdRDC:
            node.put('thresholdRDC', thresholdRDC)

        self.nodes.append(node)

    def add_forest_area_detection(self,
        nominatorBandName = None,
        denominatorBandName = None,
        windowSizeStr = None,
        T_Ratio_Low: float = None,
        T_Ratio_High: float = None
        ):
        '''
        Detect forest area.

        Parameters
        ----------
        nominatorBandName : java.lang.String
            The list of source bands.
        denominatorBandName : java.lang.String
            The list of source bands.
        windowSizeStr : java.lang.String, ['3x3', '5x5', '7x7', '9x9']
            Default '3x3'
        T_Ratio_Low : double
            The lower bound for ratio image
            Default '3.76'
        T_Ratio_High : double
            The upper bound for ratio image
            Default '6.55'
        '''

        node = Node('Forest-Area-Detection')

        if nominatorBandName:
            node.put('nominatorBandName', nominatorBandName)
        if denominatorBandName:
            node.put('denominatorBandName', denominatorBandName)
        if windowSizeStr:
            node.put('windowSizeStr', windowSizeStr)
        if T_Ratio_Low:
            node.put('T_Ratio_Low', T_Ratio_Low)
        if T_Ratio_High:
            node.put('T_Ratio_High', T_Ratio_High)

        self.nodes.append(node)

    def add_speckle_divergence(self,
        sourceBands = None,
        windowSizeStr = None
        ):
        '''
        Detect urban area.

        Parameters
        ----------
        sourceBands : java.lang.String[]
            The list of source bands.
        windowSizeStr : java.lang.String, ['3x3', '5x5', '7x7', '9x9', '11x11', '13x13', '15x15', '17x17']
            Default '15x15'
        '''

        node = Node('Speckle-Divergence')

        if sourceBands:
            node.put('sourceBands', sourceBands)
        if windowSizeStr:
            node.put('windowSizeStr', windowSizeStr)

        self.nodes.append(node)

    def add_ireci_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redB4Factor: float = None,
        redB5Factor: float = None,
        redB6Factor: float = None,
        nirFactor: float = None,
        redSourceBand4 = None,
        redSourceBand5 = None,
        redSourceBand6 = None,
        nirSourceBand = None
        ):
        '''
        Inverted red-edge chlorophyll index

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redB4Factor : float
            The value of the red source band (B4) is multiplied by this value.
            Default '1.0F'
        redB5Factor : float
            The value of the red source band (B5) is multiplied by this value.
            Default '1.0F'
        redB6Factor : float
            The value of the red source band (B6) is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand4 : java.lang.String
            The red band (B4) for the IRECI computation. If not provided, the operator will try to find the best fitting band.
        redSourceBand5 : java.lang.String
            The red band (B5) for the IRECI computation. If not provided, the operator will try to find the best fitting band.
        redSourceBand6 : java.lang.String
            The red band (B6) for the IRECI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the IRECI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('IreciOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redB4Factor:
            node.put('redB4Factor', redB4Factor)
        if redB5Factor:
            node.put('redB5Factor', redB5Factor)
        if redB6Factor:
            node.put('redB6Factor', redB6Factor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand4:
            node.put('redSourceBand4', redSourceBand4)
        if redSourceBand5:
            node.put('redSourceBand5', redSourceBand5)
        if redSourceBand6:
            node.put('redSourceBand6', redSourceBand6)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_remove_grd_border_noise(self,
        selectedPolarisations = None,
        borderLimit: int = None,
        trimThreshold: float = None
        ):
        '''
        Mask no-value pixels for GRD product

        Parameters
        ----------
        selectedPolarisations : java.lang.String[]
            The list of polarisations
        borderLimit : int
            The border margin limit
            Default '500'
        trimThreshold : double
            The trim threshold
            Default '0.5'
        '''

        node = Node('Remove-GRD-Border-Noise')

        if selectedPolarisations:
            node.put('selectedPolarisations', selectedPolarisations)
        if borderLimit:
            node.put('borderLimit', borderLimit)
        if trimThreshold:
            node.put('trimThreshold', trimThreshold)

        self.nodes.append(node)

    def add_multi_master_in_sar(self,
        orbitDegree: int = None,
        pairs = None,
        includeWavenumber: bool = None,
        includeIncidenceAngle: bool = None,
        includeLatLon: bool = None,
        cohWindowAz: int = None,
        cohWindowRg: int = None
        ):
        '''
        Multi-master InSAR processing

        Parameters
        ----------
        orbitDegree : int, ['1', '2', '3', '4', '5']
            Degree of orbit (polynomial) interpolator
            Default '4'
        pairs : java.lang.String[]
            List of interferometric pairs
        includeWavenumber : boolean
            Default 'true'
        includeIncidenceAngle : boolean
            Default 'true'
        includeLatLon : boolean
            Default 'true'
        cohWindowAz : int
            Size of coherence estimation window in azimuth
            Default '10'
        cohWindowRg : int
            Size of coherence estimation window in range
            Default '10'
        '''

        node = Node('MultiMasterInSAR')

        if orbitDegree:
            node.put('orbitDegree', orbitDegree)
        if pairs:
            node.put('pairs', pairs)
        if includeWavenumber:
            node.put('includeWavenumber', includeWavenumber)
        if includeIncidenceAngle:
            node.put('includeIncidenceAngle', includeIncidenceAngle)
        if includeLatLon:
            node.put('includeLatLon', includeLatLon)
        if cohWindowAz:
            node.put('cohWindowAz', cohWindowAz)
        if cohWindowRg:
            node.put('cohWindowRg', cohWindowRg)

        self.nodes.append(node)

    def add_object_discrimination(self,
        minTargetSizeInMeter: float = None,
        maxTargetSizeInMeter: float = None
        ):
        '''
        Remove false alarms from the detected objects.

        Parameters
        ----------
        minTargetSizeInMeter : double
            Minimum target size
            Default '50.0'
        maxTargetSizeInMeter : double
            Maximum target size
            Default '600.0'
        '''

        node = Node('Object-Discrimination')

        if minTargetSizeInMeter:
            node.put('minTargetSizeInMeter', minTargetSizeInMeter)
        if maxTargetSizeInMeter:
            node.put('maxTargetSizeInMeter', maxTargetSizeInMeter)

        self.nodes.append(node)

    def add_update_geo_reference(self,
        sourceBandNames = None,
        demName = None,
        demResamplingMethod = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        reGridMethod: bool = None
        ):
        '''
        Update Geo Reference

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        demName : java.lang.String, ['ACE', 'ASTER 1sec GDEM', 'GETASSE30', 'SRTM 1Sec HGT', 'SRTM 3Sec']
            The digital elevation model.
            Default 'SRTM 3Sec'
        demResamplingMethod : java.lang.String
            Default 'BICUBIC_INTERPOLATION'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        reGridMethod : boolean
            Default 'false'
        '''

        node = Node('Update-Geo-Reference')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if demName:
            node.put('demName', demName)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if reGridMethod:
            node.put('reGridMethod', reGridMethod)

        self.nodes.append(node)

    def add_multi_master_stack_generator(self,
        outputFolder = None
        ):
        '''
        Generates a set of master-slave pairs from a coregistered stack for use in SBAS processing

        Parameters
        ----------
        outputFolder : java.lang.String
            Output folder
        '''

        node = Node('MultiMasterStackGenerator')

        if outputFolder:
            node.put('outputFolder', outputFolder)

        self.nodes.append(node)

    def add_product_set_reader(self,
        fileList = None
        ):
        '''
        Adds a list of sources

        Parameters
        ----------
        fileList : java.lang.String[]
        '''

        node = Node('ProductSet-Reader')

        if fileList:
            node.put('fileList', fileList)

        self.nodes.append(node)

    def add_emcluster_analysis(self,
        clusterCount: int = None,
        iterationCount: int = None,
        randomSeed: int = None,
        sourceBandNames = None,
        roiMaskName = None,
        includeProbabilityBands: bool = None
        ):
        '''
        Performs an expectation-maximization (EM) cluster analysis.

        Parameters
        ----------
        clusterCount : int
            Number of clusters
            Default '14'
        iterationCount : int
            Number of iterations
            Default '30'
        randomSeed : int
            Seed for the random generator, used for initialising the algorithm.
            Default '31415'
        sourceBandNames : java.lang.String[]
            The names of the bands being used for the cluster analysis.
        roiMaskName : java.lang.String
            The name of the ROI-Mask that should be used.
        includeProbabilityBands : boolean
            Determines whether the posterior probabilities are included as band data.
            Default 'false'
        '''

        node = Node('EMClusterAnalysis')

        if clusterCount:
            node.put('clusterCount', clusterCount)
        if iterationCount:
            node.put('iterationCount', iterationCount)
        if randomSeed:
            node.put('randomSeed', randomSeed)
        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if roiMaskName:
            node.put('roiMaskName', roiMaskName)
        if includeProbabilityBands:
            node.put('includeProbabilityBands', includeProbabilityBands)

        self.nodes.append(node)

    def add_meris_gaseous_correction(self,
        copyAllTiePoints: bool = None,
        correctWater: bool = None,
        exportTg: bool = None
        ):
        '''
        MERIS L2 gaseous absorbtion correction.

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        correctWater : boolean
        exportTg : boolean
        '''

        node = Node('Meris.GaseousCorrection')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if correctWater:
            node.put('correctWater', correctWater)
        if exportTg:
            node.put('exportTg', exportTg)

        self.nodes.append(node)

    def add_band_select(self,
        selectedPolarisations = None,
        sourceBandNames = None,
        bandNamePattern = None
        ):
        '''
        Creates a new product with only selected bands

        Parameters
        ----------
        selectedPolarisations : java.lang.String[]
            The list of polarisations
        sourceBandNames : java.lang.String[]
            The list of source bands.
        bandNamePattern : java.lang.String
            Band name regular expression pattern
        '''

        node = Node('BandSelect')

        if selectedPolarisations:
            node.put('selectedPolarisations', selectedPolarisations)
        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if bandNamePattern:
            node.put('bandNamePattern', bandNamePattern)

        self.nodes.append(node)

    def add_s2resampling(self,
        targetResolution = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        flagDownsamplingMethod = None,
        resampleOnPyramidLevels: bool = None
        ):
        '''
        Specific S2 resample algorithm

        Parameters
        ----------
        targetResolution : java.lang.String, ['10', '20', '60']
            The output resolution.
            Default '60'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Bilinear'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'Mean'
        flagDownsamplingMethod : java.lang.String, ['First', 'FlagAnd', 'FlagOr', 'FlagMedianAnd', 'FlagMedianOr']
            The method used for aggregation (downsampling to a coarser resolution) of flags.
            Default 'First'
        resampleOnPyramidLevels : boolean
            This setting will increase performance when viewing the image, but accurate resamplings are only retrieved when zooming in on a pixel.
            Default 'true'
        '''

        node = Node('S2Resampling')

        if targetResolution:
            node.put('targetResolution', targetResolution)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if flagDownsamplingMethod:
            node.put('flagDownsamplingMethod', flagDownsamplingMethod)
        if resampleOnPyramidLevels:
            node.put('resampleOnPyramidLevels', resampleOnPyramidLevels)

        self.nodes.append(node)

    def add_glcm(self,
        sourceBands = None,
        windowSizeStr = None,
        angleStr = None,
        quantizerStr = None,
        quantizationLevelsStr = None,
        displacement: int = None,
        noDataValue: float = None,
        outputContrast = None,
        outputDissimilarity = None,
        outputHomogeneity = None,
        outputASM = None,
        outputEnergy = None,
        outputMAX = None,
        outputEntropy = None,
        outputMean = None,
        outputVariance = None,
        outputCorrelation = None
        ):
        '''
        Extract Texture Features

        Parameters
        ----------
        sourceBands : java.lang.String[]
            The list of source bands.
        windowSizeStr : java.lang.String, ['5x5', '7x7', '9x9', '11x11', '13x13', '15x15', '17x17', '21x21']
            Default '9x9'
        angleStr : java.lang.String, ['0', '45', '90', '135', 'ALL']
            Default 'ALL'
        quantizerStr : java.lang.String, ['Equal Distance Quantizer', 'Probabilistic Quantizer']
            Default 'Probabilistic Quantizer'
        quantizationLevelsStr : java.lang.String, ['8', '16', '32', '64', '128']
            Default '32'
        displacement : int
            Pixel displacement
            Default '4'
        noDataValue : double
            Target product no data value
            Default '-9999.0'
        outputContrast : java.lang.Boolean
            Output Contrast
            Default 'true'
        outputDissimilarity : java.lang.Boolean
            Output Dissimilarity
            Default 'true'
        outputHomogeneity : java.lang.Boolean
            Output Homogeneity
            Default 'true'
        outputASM : java.lang.Boolean
            Output Angular Second Moment
            Default 'true'
        outputEnergy : java.lang.Boolean
            Output Energy
            Default 'true'
        outputMAX : java.lang.Boolean
            Output Maximum Probability
            Default 'true'
        outputEntropy : java.lang.Boolean
            Output Entropy
            Default 'true'
        outputMean : java.lang.Boolean
            Output GLCM Mean
            Default 'true'
        outputVariance : java.lang.Boolean
            Output GLCM Variance
            Default 'true'
        outputCorrelation : java.lang.Boolean
            Output GLCM Correlation
            Default 'true'
        '''

        node = Node('GLCM')

        if sourceBands:
            node.put('sourceBands', sourceBands)
        if windowSizeStr:
            node.put('windowSizeStr', windowSizeStr)
        if angleStr:
            node.put('angleStr', angleStr)
        if quantizerStr:
            node.put('quantizerStr', quantizerStr)
        if quantizationLevelsStr:
            node.put('quantizationLevelsStr', quantizationLevelsStr)
        if displacement:
            node.put('displacement', displacement)
        if noDataValue:
            node.put('noDataValue', noDataValue)
        if outputContrast:
            node.put('outputContrast', outputContrast)
        if outputDissimilarity:
            node.put('outputDissimilarity', outputDissimilarity)
        if outputHomogeneity:
            node.put('outputHomogeneity', outputHomogeneity)
        if outputASM:
            node.put('outputASM', outputASM)
        if outputEnergy:
            node.put('outputEnergy', outputEnergy)
        if outputMAX:
            node.put('outputMAX', outputMAX)
        if outputEntropy:
            node.put('outputEntropy', outputEntropy)
        if outputMean:
            node.put('outputMean', outputMean)
        if outputVariance:
            node.put('outputVariance', outputVariance)
        if outputCorrelation:
            node.put('outputCorrelation', outputCorrelation)

        self.nodes.append(node)

    def add_azimuth_filter(self,
        fftLength: int = None,
        aziFilterOverlap: int = None,
        alphaHamming: float = None
        ):
        '''
        Azimuth Filter

        Parameters
        ----------
        fftLength : int, ['64', '128', '256', '512', '1024', '2048']
            Length of filtering window
            Default '256'
        aziFilterOverlap : int, ['0', '8', '16', '32', '64', '128', '256']
            Overlap between filtering windows in azimuth direction [lines]
            Default '0'
        alphaHamming : float, ['0.5', '0.75', '0.8', '0.9', '1']
            Weight for Hamming filter (1 is rectangular window)
            Default '0.75'
        '''

        node = Node('AzimuthFilter')

        if fftLength:
            node.put('fftLength', fftLength)
        if aziFilterOverlap:
            node.put('aziFilterOverlap', aziFilterOverlap)
        if alphaHamming:
            node.put('alphaHamming', alphaHamming)

        self.nodes.append(node)

    def add_arc_sst(self,
        tcwvExpression = None,
        asdi: bool = None,
        asdiCoefficientsFile = None,
        asdiMaskExpression = None,
        dual: bool = None,
        dualCoefficientsFile = None,
        dualMaskExpression = None,
        nadir: bool = None,
        nadirCoefficientsFile = None,
        nadirMaskExpression = None,
        invalidSstValue: float = None
        ):
        '''
        Computes sea surface temperature (SST) from (A)ATSR and SLSTR products.

        Parameters
        ----------
        tcwvExpression : java.lang.String
            TCWV value to use in SST retrieval
            Default '30.0'
        asdi : boolean
            Enables/disables generation of ATSR Saharan Dust Index
            Default 'true'
        asdiCoefficientsFile : org.esa.s3tbx.arc.ArcFiles, ['ASDI_ATSR1', 'ASDI_ATSR2', 'ASDI_AATSR']
            Coefficient file for ASDI
            Default 'ASDI_AATSR'
        asdiMaskExpression : java.lang.String
            ROI-mask used for the ASDI
        dual : boolean
            Enables/disables generation of the dual-view SST
            Default 'true'
        dualCoefficientsFile : org.esa.s3tbx.arc.ArcFiles, ['ARC_D2_ATSR1', 'ARC_D2_ATSR2', 'ARC_D2_AATSR', 'ARC_D2_SLSTR', 'ARC_D3_ATSR1', 'ARC_D3_ATSR2', 'ARC_D3_AATSR', 'ARC_D3_SLSTR']
            Coefficient file for the dual-view SST
            Default 'ARC_D2_AATSR'
        dualMaskExpression : java.lang.String
            ROI-mask used for the dual-view SST
        nadir : boolean
            Enables/disables generation of the nadir-view SST
            Default 'true'
        nadirCoefficientsFile : org.esa.s3tbx.arc.ArcFiles, ['ARC_N2_ATSR1', 'ARC_N2_ATSR2', 'ARC_N2_AATSR', 'ARC_N2_SLSTR', 'ARC_N3_ATSR1', 'ARC_N3_ATSR2', 'ARC_N3_AATSR', 'ARC_N3_SLSTR']
            Coefficient file for the nadir-view SST
            Default 'ARC_N2_AATSR'
        nadirMaskExpression : java.lang.String
            ROI-mask used for the nadir-view SST
        invalidSstValue : float
            Value used to fill invalid SST pixels
            Default '-999.0f'
        '''

        node = Node('Arc.SST')

        if tcwvExpression:
            node.put('tcwvExpression', tcwvExpression)
        if asdi:
            node.put('asdi', asdi)
        if asdiCoefficientsFile:
            node.put('asdiCoefficientsFile', asdiCoefficientsFile)
        if asdiMaskExpression:
            node.put('asdiMaskExpression', asdiMaskExpression)
        if dual:
            node.put('dual', dual)
        if dualCoefficientsFile:
            node.put('dualCoefficientsFile', dualCoefficientsFile)
        if dualMaskExpression:
            node.put('dualMaskExpression', dualMaskExpression)
        if nadir:
            node.put('nadir', nadir)
        if nadirCoefficientsFile:
            node.put('nadirCoefficientsFile', nadirCoefficientsFile)
        if nadirMaskExpression:
            node.put('nadirMaskExpression', nadirMaskExpression)
        if invalidSstValue:
            node.put('invalidSstValue', invalidSstValue)

        self.nodes.append(node)

    def add_sar_mosaic(self,
        sourceBandNames = None,
        resamplingMethod = None,
        average = None,
        normalizeByMean = None,
        gradientDomainMosaic = None,
        pixelSize: float = None,
        sceneWidth: int = None,
        sceneHeight: int = None,
        feather: int = None,
        maxIterations: int = None,
        convergenceThreshold: float = None
        ):
        '''
        Mosaics two or more products based on their geo-codings.

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        resamplingMethod : java.lang.String, ['NEAREST_NEIGHBOUR', 'BILINEAR_INTERPOLATION', 'CUBIC_CONVOLUTION']
            The method to be used when resampling the slave grid onto the master grid.
            Default 'NEAREST_NEIGHBOUR'
        average : java.lang.Boolean
            Average the overlapping areas
            Default 'true'
        normalizeByMean : java.lang.Boolean
            Normalize by Mean
            Default 'true'
        gradientDomainMosaic : java.lang.Boolean
            Gradient Domain Mosaic
            Default 'false'
        pixelSize : double
            Pixel Size (m)
            Default '0'
        sceneWidth : int
            Target width
            Default '0'
        sceneHeight : int
            Target height
            Default '0'
        feather : int
            Feather amount around source image
            Default '0'
        maxIterations : int
            Maximum number of iterations
            Default '5000'
        convergenceThreshold : double
            Convergence threshold for Relaxed Gauss-Seidel method
            Default '1e-4'
        '''

        node = Node('SAR-Mosaic')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if resamplingMethod:
            node.put('resamplingMethod', resamplingMethod)
        if average:
            node.put('average', average)
        if normalizeByMean:
            node.put('normalizeByMean', normalizeByMean)
        if gradientDomainMosaic:
            node.put('gradientDomainMosaic', gradientDomainMosaic)
        if pixelSize:
            node.put('pixelSize', pixelSize)
        if sceneWidth:
            node.put('sceneWidth', sceneWidth)
        if sceneHeight:
            node.put('sceneHeight', sceneHeight)
        if feather:
            node.put('feather', feather)
        if maxIterations:
            node.put('maxIterations', maxIterations)
        if convergenceThreshold:
            node.put('convergenceThreshold', convergenceThreshold)

        self.nodes.append(node)

    def add_double_difference_interferogram(self,
        outputCoherence: bool = None,
        cohWinSize = None
        ):
        '''
        Compute double difference interferogram

        Parameters
        ----------
        outputCoherence : boolean
            Output coherence for overlapped area
            Default 'false'
        cohWinSize : java.lang.String, ['3', '5', '9', '11']
            Default '5'
        '''

        node = Node('Double-Difference-Interferogram')

        if outputCoherence:
            node.put('outputCoherence', outputCoherence)
        if cohWinSize:
            node.put('cohWinSize', cohWinSize)

        self.nodes.append(node)

    def add_bi2_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        greenFactor: float = None,
        nirFactor: float = None,
        redSourceBand = None,
        greenSourceBand = None,
        nirSourceBand = None
        ):
        '''
        The second Brightness index represents the average of the brightness of a satellite image.

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the RED source band is multiplied by this value.
            Default '1.0F'
        greenFactor : float
            The value of the GREEN source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the BI2 computation. If not provided, the operator will try to find the best fitting band.
        greenSourceBand : java.lang.String
            The green band for the BI2 computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the BI2 computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('Bi2Op')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if greenFactor:
            node.put('greenFactor', greenFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if greenSourceBand:
            node.put('greenSourceBand', greenSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_ri_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        greenFactor: float = None,
        redSourceBand = None,
        greenSourceBand = None
        ):
        '''
        The Redness Index was developed to identify soil colour variations.

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        greenFactor : float
            The value of the green source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the RI computation. If not provided, the operator will try to find the best fitting band.
        greenSourceBand : java.lang.String
            The green band for the RI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('RiOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if greenFactor:
            node.put('greenFactor', greenFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if greenSourceBand:
            node.put('greenSourceBand', greenSourceBand)

        self.nodes.append(node)

    def add_olci_anomaly_flagging(self,
        writeSlopeInformation: bool = None
        ):
        '''
        Adds a flagging band indicating saturated pixels and altitude data overflows

        Parameters
        ----------
        writeSlopeInformation : boolean
            If set to true, the operator adds two bands containing the maximal spectral slope and the band index where the peak is observed.
            Default 'false'
        '''

        node = Node('OlciAnomalyFlagging')

        if writeSlopeInformation:
            node.put('writeSlopeInformation', writeSlopeInformation)

        self.nodes.append(node)

    def add_gabor_filter(self,
        sourceBandNames = None,
        theta: float = None
        ):
        '''
        Extract Texture Features

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        theta : double
        '''

        node = Node('GaborFilter')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if theta:
            node.put('theta', theta)

        self.nodes.append(node)

    def add_ellipsoid_correction_gg(self,
        sourceBandNames = None,
        imgResamplingMethod = None,
        mapProjection = None
        ):
        '''
        GG method for orthorectification

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        imgResamplingMethod : java.lang.String, ['NEAREST_NEIGHBOUR', 'BILINEAR_INTERPOLATION', 'CUBIC_CONVOLUTION']
            Default 'BILINEAR_INTERPOLATION'
        mapProjection : java.lang.String
            The coordinate reference system in well known text format
            Default 'WGS84(DD)'
        '''

        node = Node('Ellipsoid-Correction-GG')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if imgResamplingMethod:
            node.put('imgResamplingMethod', imgResamplingMethod)
        if mapProjection:
            node.put('mapProjection', mapProjection)

        self.nodes.append(node)

    def add_pix_ex(self,
        sourceProductPaths = None,
        exportBands = None,
        exportTiePoints = None,
        exportMasks = None,
        coordinates = None,
        timeDifference = None,
        coordinatesFile = None,
        matchupFile = None,
        windowSize = None,
        outputDir = None,
        outputFilePrefix = None,
        expression = None,
        exportExpressionResult = None,
        aggregatorStrategyType = None,
        exportSubScenes: bool = None,
        subSceneBorderSize: int = None,
        exportKmz: bool = None,
        extractTimeFromFilename: bool = None,
        dateInterpretationPattern = None,
        filenameInterpretationPattern = None,
        includeOriginalInput: bool = None,
        scatterPlotVariableCombinations = None
        ):
        '''
        Extracts pixels from given locations and source products.

        Parameters
        ----------
        sourceProductPaths : java.lang.String[]
            A comma-separated list of file paths specifying the source products.
            Each path may contain the wildcards '**' (matches recursively any directory),
            '*' (matches any character sequence in path names) and
            '?' (matches any single character).
        exportBands : java.lang.Boolean
            Specifies if bands are to be exported
            Default 'true'
        exportTiePoints : java.lang.Boolean
            Specifies if tie-points are to be exported
            Default 'true'
        exportMasks : java.lang.Boolean
            Specifies if masks are to be exported
            Default 'true'
        coordinates : org.esa.snap.pixex.Coordinate[]
            The geo-coordinates
        timeDifference : java.lang.String
            The acceptable time difference compared to the time given for a coordinate.
            The format is a number followed by (D)ay, (H)our or (M)inute. If no time difference is provided, all input products are considered regardless of their time.
        coordinatesFile : java.io.File
            Path to a file containing geo-coordinates. BEAM's placemark files can be used.
        matchupFile : java.io.File
            Path to a CSV-file containing geo-coordinates associated with measurements accordingto BEAM CSV format specification
        windowSize : java.lang.Integer
            Side length of surrounding window (uneven)
            Default '1'
        outputDir : java.io.File
            The output directory.
        outputFilePrefix : java.lang.String
            The prefix is used to name the output files.
            Default 'pixEx'
        expression : java.lang.String
            Band maths expression (optional). Defines valid pixels.
        exportExpressionResult : java.lang.Boolean
            If true, the expression result is exported per pixel, otherwise the expression 
            is used as filter (all pixels in given window must be valid).
            Default 'true'
        aggregatorStrategyType : java.lang.String, ['no aggregation', 'mean', 'min', 'max', 'median']
            If the window size is larger than 1, this parameter describes by which method a single 
            value shall be derived from the pixels.
            Default 'no aggregation'
        exportSubScenes : boolean
            If set to true, sub-scenes of the regions, where pixels are found, are exported.
            Default 'false'
        subSceneBorderSize : int
            An additional border around the region where pixels are found.
            Default '0'
        exportKmz : boolean
            If set to true, a Google KMZ file will be created, which contains the coordinates where pixels are found.
            Default 'false'
        extractTimeFromFilename : boolean
            If set to true, the sensing start and sensing stop should be extracted from the filename of each input product.
            Default 'false'
        dateInterpretationPattern : java.lang.String
            Describes how a date/time section inside a product filename should be interpreted. E.G. yyyyMMdd_HHmmss
            Default 'yyyyMMdd'
        filenameInterpretationPattern : java.lang.String
            Describes how the filename of a product should be interpreted.
            Default '*${startDate}*${endDate}*'
        includeOriginalInput : boolean
            Determines if the original input measurements shall be included in the output.
            Default 'false'
        scatterPlotVariableCombinations : org.esa.snap.pixex.PixExOp$VariableCombination[]
            Array of 2-tuples of variable names; for each of these tuples a scatter plot will be exported.
        '''

        node = Node('PixEx')

        if sourceProductPaths:
            node.put('sourceProductPaths', sourceProductPaths)
        if exportBands:
            node.put('exportBands', exportBands)
        if exportTiePoints:
            node.put('exportTiePoints', exportTiePoints)
        if exportMasks:
            node.put('exportMasks', exportMasks)
        if coordinates:
            node.put('coordinates', coordinates)
        if timeDifference:
            node.put('timeDifference', timeDifference)
        if coordinatesFile:
            node.put('coordinatesFile', coordinatesFile)
        if matchupFile:
            node.put('matchupFile', matchupFile)
        if windowSize:
            node.put('windowSize', windowSize)
        if outputDir:
            node.put('outputDir', outputDir)
        if outputFilePrefix:
            node.put('outputFilePrefix', outputFilePrefix)
        if expression:
            node.put('expression', expression)
        if exportExpressionResult:
            node.put('exportExpressionResult', exportExpressionResult)
        if aggregatorStrategyType:
            node.put('aggregatorStrategyType', aggregatorStrategyType)
        if exportSubScenes:
            node.put('exportSubScenes', exportSubScenes)
        if subSceneBorderSize:
            node.put('subSceneBorderSize', subSceneBorderSize)
        if exportKmz:
            node.put('exportKmz', exportKmz)
        if extractTimeFromFilename:
            node.put('extractTimeFromFilename', extractTimeFromFilename)
        if dateInterpretationPattern:
            node.put('dateInterpretationPattern', dateInterpretationPattern)
        if filenameInterpretationPattern:
            node.put('filenameInterpretationPattern', filenameInterpretationPattern)
        if includeOriginalInput:
            node.put('includeOriginalInput', includeOriginalInput)
        if scatterPlotVariableCombinations:
            node.put('scatterPlotVariableCombinations', scatterPlotVariableCombinations)

        self.nodes.append(node)

    def add_ionospheric_correction(self,
        sigma: int = None,
        coherenceThreshold: float = None,
        minCoherence: float = None
        ):
        '''
        Estimation of Ionospheric Phase Screens

        Parameters
        ----------
        sigma : int
            Standard deviation for Gaussian filter
            Default '81'
        coherenceThreshold : double
            Coherence threshold
            Default '0.6'
        minCoherence : double
            Minimum coherence for output mask
            Default '0.2'
        '''

        node = Node('IonosphericCorrection')

        if sigma:
            node.put('sigma', sigma)
        if coherenceThreshold:
            node.put('coherenceThreshold', coherenceThreshold)
        if minCoherence:
            node.put('minCoherence', minCoherence)

        self.nodes.append(node)

    def add_mph_chl_olci(self,
        validPixelExpression = None,
        cyanoMaxValue: float = None,
        chlThreshForFloatFlag: float = None,
        exportMph: bool = None
        ):
        '''
        Computes maximum peak height of chlorophyll for OLCI. Implements OLCI-specific parts.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Expression defining pixels considered for processing.
        cyanoMaxValue : double
            Maximum chlorophyll, arithmetically higher values are capped.
            Default '1000.0'
        chlThreshForFloatFlag : double
            Chlorophyll threshold, above which all cyanobacteria dominated waters are 'float.
            Default '350.0'
        exportMph : boolean
            Switch to true to write 'mph' band.
            Default 'false'
        '''

        node = Node('MphChlOlci')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if cyanoMaxValue:
            node.put('cyanoMaxValue', cyanoMaxValue)
        if chlThreshForFloatFlag:
            node.put('chlThreshForFloatFlag', chlThreshForFloatFlag)
        if exportMph:
            node.put('exportMph', exportMph)

        self.nodes.append(node)

    def addc2rcc_modis(self,
        validPixelExpression = None,
        salinity: float = None,
        temperature: float = None,
        ozone: float = None,
        press: float = None,
        atmosphericAuxDataPath = None,
        outputRtosa: bool = None,
        outputAsRrs: bool = None,
        outputAngles: bool = None
        ):
        '''
        Performs atmospheric correction and IOP retrieval on MODIS L1C_LAC data products.

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Defines the pixels which are valid for processing
            Default '!(l2_flags.LAND ||  max(rhot_412,max(rhot_443,max(rhot_488,max(rhot_531,max(rhot_547,max(rhot_555,max(rhot_667,max(rhot_678,max(rhot_748,rhot_869)))))))))>0.25)'
        salinity : double
            The value used as salinity for the scene
            Default '35.0'
        temperature : double
            The value used as temperature for the scene
            Default '15.0'
        ozone : double
            The value used as ozone if not provided by auxiliary data
            Default '330'
        press : double
            The surface air pressure at sea level if not provided by auxiliary data
            Default '1000'
        atmosphericAuxDataPath : java.lang.String
            Path to the atmospheric auxiliary data directory. Use either this or the specific products. If the auxiliary data needed for interpolation is not available in this path, the data will automatically downloaded.
        outputRtosa : boolean
            Default 'false'
        outputAsRrs : boolean
            Reflectance values in the target product shall be either written as remote sensing or water leaving reflectances
            Default 'false'
        outputAngles : boolean
            Default 'false'
        '''

        node = Node('c2rcc.modis')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if salinity:
            node.put('salinity', salinity)
        if temperature:
            node.put('temperature', temperature)
        if ozone:
            node.put('ozone', ozone)
        if press:
            node.put('press', press)
        if atmosphericAuxDataPath:
            node.put('atmosphericAuxDataPath', atmosphericAuxDataPath)
        if outputRtosa:
            node.put('outputRtosa', outputRtosa)
        if outputAsRrs:
            node.put('outputAsRrs', outputAsRrs)
        if outputAngles:
            node.put('outputAngles', outputAngles)

        self.nodes.append(node)

    def add_tile_cache(self,
        cacheSize: int = None
        ):
        '''
        Experimental Operator which provides a dedicated cache for its source product.
A guide on how this operator is used is provided at https://senbox.atlassian.net/wiki/x/VQCTLw.

        Parameters
        ----------
        cacheSize : int
            The cache size in MB. Set it to 0 to use default tile cache.
            Default '1000'
        '''

        node = Node('TileCache')

        if cacheSize:
            node.put('cacheSize', cacheSize)

        self.nodes.append(node)

    def add_apply_orbit_file(self,
        orbitType = None,
        polyDegree: int = None,
        continueOnFail = None
        ):
        '''
        Apply orbit file

        Parameters
        ----------
        orbitType : java.lang.String, ['Sentinel Precise (Auto Download)', 'Sentinel Restituted (Auto Download)', 'DORIS Preliminary POR (ENVISAT)', 'DORIS Precise VOR (ENVISAT) (Auto Download)', 'DELFT Precise (ENVISAT, ERS1&2) (Auto Download)', 'PRARE Precise (ERS1&2) (Auto Download)', 'Kompsat5 Precise']
            Default 'Sentinel Precise (Auto Download)'
        polyDegree : int
            Default '3'
        continueOnFail : java.lang.Boolean
            Default 'false'
        '''

        node = Node('Apply-Orbit-File')

        if orbitType:
            node.put('orbitType', orbitType)
        if polyDegree:
            node.put('polyDegree', polyDegree)
        if continueOnFail:
            node.put('continueOnFail', continueOnFail)

        self.nodes.append(node)

    def add_remodulate(self
        ):
        '''
        Remodulation and reramping of SLC data

        Parameters
        ----------
        '''

        node = Node('Remodulate')


        self.nodes.append(node)

    def add_mtci_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redB4Factor: float = None,
        redB5Factor: float = None,
        nirFactor: float = None,
        redSourceBand4 = None,
        redSourceBand5 = None,
        nirSourceBand = None
        ):
        '''
        The Meris Terrestrial Chlorophyll Index estimates the Red Edge Position (REP).

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redB4Factor : float
            The value of the red source band (B4) is multiplied by this value.
            Default '1.0F'
        redB5Factor : float
            The value of the red source band (B5) is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand4 : java.lang.String
            The red band (B4) for the MTCI computation. If not provided, the operator will try to find the best fitting band.
        redSourceBand5 : java.lang.String
            The red band (B5) for the MTCI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the MTCI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('MtciOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redB4Factor:
            node.put('redB4Factor', redB4Factor)
        if redB5Factor:
            node.put('redB5Factor', redB5Factor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand4:
            node.put('redSourceBand4', redSourceBand4)
        if redSourceBand5:
            node.put('redSourceBand5', redSourceBand5)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_band_merge(self,
        sourceBandNames = None,
        geographicError: float = None
        ):
        '''
        Allows copying raster data from any number of source products to a specified 'master' product.

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        geographicError : float
            Defines the maximum lat/lon error in degree between the products.
            Default '1.0E-5f'
        '''

        node = Node('BandMerge')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if geographicError:
            node.put('geographicError', geographicError)

        self.nodes.append(node)

    def add_biophysical_landsat8_op(self,
        computeLAI: bool = None,
        computeFapar: bool = None,
        computeFcover: bool = None
        ):
        '''
        The 'Biophysical Processor' operator retrieves LAI from atmospherically corrected Landsat8 products

        Parameters
        ----------
        computeLAI : boolean
            Compute LAI (Leaf Area Index)
            Default 'true'
        computeFapar : boolean
            Compute FAPAR (Fraction of Absorbed Photosynthetically Active Radiation)
            Default 'true'
        computeFcover : boolean
            Compute FVC (Fraction of Vegetation Cover)
            Default 'true'
        '''

        node = Node('BiophysicalLandsat8Op')

        if computeLAI:
            node.put('computeLAI', computeLAI)
        if computeFapar:
            node.put('computeFapar', computeFapar)
        if computeFcover:
            node.put('computeFcover', computeFcover)

        self.nodes.append(node)

    def add_mph_chl(self,
        validPixelExpression = None,
        cyanoMaxValue: float = None,
        chlThreshForFloatFlag: float = None,
        exportMph: bool = None,
        applyLowPassFilter: bool = None
        ):
        '''
        This operator computes maximum peak height of chlorophyll (MPH/CHL).

        Parameters
        ----------
        validPixelExpression : java.lang.String
            Expression defining pixels considered for processing. If not set, all valid pixels over water are processed.
        cyanoMaxValue : double
            Maximum chlorophyll, arithmetically higher values are capped.
            Default '1000.0'
        chlThreshForFloatFlag : double
            Chlorophyll threshold, above which all cyanobacteria dominated waters are 'float'.
            Default '500.0'
        exportMph : boolean
            Switch to true to write 'mph' band.
            Default 'false'
        applyLowPassFilter : boolean
            Switch to true to apply a 3x3 low-pass filter on the result.
            Default 'false'
        '''

        node = Node('MphChl')

        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if cyanoMaxValue:
            node.put('cyanoMaxValue', cyanoMaxValue)
        if chlThreshForFloatFlag:
            node.put('chlThreshForFloatFlag', chlThreshForFloatFlag)
        if exportMph:
            node.put('exportMph', exportMph)
        if applyLowPassFilter:
            node.put('applyLowPassFilter', applyLowPassFilter)

        self.nodes.append(node)

    def add_topsar_deburst(self,
        selectedPolarisations = None
        ):
        '''
        Debursts a Sentinel-1 TOPSAR product

        Parameters
        ----------
        selectedPolarisations : java.lang.String[]
            The list of polarisations
        '''

        node = Node('TOPSAR-Deburst')

        if selectedPolarisations:
            node.put('selectedPolarisations', selectedPolarisations)

        self.nodes.append(node)

    def add_minimum_distance_classifier(self,
        numTrainSamples: int = None,
        savedClassifierName = None,
        doLoadClassifier = None,
        doClassValQuantization = None,
        minClassValue = None,
        classValStepSize = None,
        classLevels: int = None,
        trainingBands = None,
        trainOnRaster = None,
        trainingVectors = None,
        featureBands = None,
        labelSource = None,
        evaluateClassifier = None,
        evaluateFeaturePowerSet = None,
        minPowerSetSize = None,
        maxPowerSetSize = None
        ):
        '''
        Minimum Distance classifier

        Parameters
        ----------
        numTrainSamples : int
            The number of training samples
            Default '5000'
        savedClassifierName : java.lang.String
            The saved classifier name
        doLoadClassifier : java.lang.Boolean
            Choose to save or load classifier
            Default 'false'
        doClassValQuantization : java.lang.Boolean
            Quantization for raster traiing
            Default 'true'
        minClassValue : java.lang.Double
            Quantization min class value for raster traiing
            Default '0.0'
        classValStepSize : java.lang.Double
            Quantization step size for raster traiing
            Default '5.0'
        classLevels : int
            Quantization class levels for raster traiing
            Default '101'
        trainingBands : java.lang.String[]
            Raster bands to train on
        trainOnRaster : java.lang.Boolean
            Train on raster or vector data
            Default 'true'
        trainingVectors : java.lang.String[]
            Vectors to train on
        featureBands : java.lang.String[]
            Names of bands to be used as features
        labelSource : java.lang.String
            'VectorNodeName' or specific Attribute name
        evaluateClassifier : java.lang.Boolean
            Evaluate classifier and features
        evaluateFeaturePowerSet : java.lang.Boolean
            Evaluate the power set of features
            Default 'false'
        minPowerSetSize : java.lang.Integer
            Minimum size of the power set of features
            Default '2'
        maxPowerSetSize : java.lang.Integer
            Maximum size of the power set of features
            Default '7'
        '''

        node = Node('Minimum-Distance-Classifier')

        if numTrainSamples:
            node.put('numTrainSamples', numTrainSamples)
        if savedClassifierName:
            node.put('savedClassifierName', savedClassifierName)
        if doLoadClassifier:
            node.put('doLoadClassifier', doLoadClassifier)
        if doClassValQuantization:
            node.put('doClassValQuantization', doClassValQuantization)
        if minClassValue:
            node.put('minClassValue', minClassValue)
        if classValStepSize:
            node.put('classValStepSize', classValStepSize)
        if classLevels:
            node.put('classLevels', classLevels)
        if trainingBands:
            node.put('trainingBands', trainingBands)
        if trainOnRaster:
            node.put('trainOnRaster', trainOnRaster)
        if trainingVectors:
            node.put('trainingVectors', trainingVectors)
        if featureBands:
            node.put('featureBands', featureBands)
        if labelSource:
            node.put('labelSource', labelSource)
        if evaluateClassifier:
            node.put('evaluateClassifier', evaluateClassifier)
        if evaluateFeaturePowerSet:
            node.put('evaluateFeaturePowerSet', evaluateFeaturePowerSet)
        if minPowerSetSize:
            node.put('minPowerSetSize', minPowerSetSize)
        if maxPowerSetSize:
            node.put('maxPowerSetSize', maxPowerSetSize)

        self.nodes.append(node)

    def add_rad2_refl(self,
        sensor = None,
        conversionMode = None,
        copyTiePointGrids: bool = None,
        copyFlagBandsAndMasks: bool = None,
        copyNonSpectralBands: bool = None
        ):
        '''
        Provides conversion from radiances to reflectances or backwards.

        Parameters
        ----------
        sensor : org.esa.s3tbx.processor.rad2refl.Sensor, ['MERIS', 'OLCI', 'SLSTR_500m']
            The sensor
            Default 'OLCI'
        conversionMode : java.lang.String, ['RAD_TO_REFL', 'REFL_TO_RAD']
            Conversion mode: from rad to refl, or backwards
            Default 'RAD_TO_REFL'
        copyTiePointGrids : boolean
            If set, all tie point grids from source product are written to target product
            Default 'false'
        copyFlagBandsAndMasks : boolean
            If set, all flag bands and masks from source product are written to target product
            Default 'false'
        copyNonSpectralBands : boolean
            If set, all other non-spectral bands from source product are written to target product
            Default 'false'
        '''

        node = Node('Rad2Refl')

        if sensor:
            node.put('sensor', sensor)
        if conversionMode:
            node.put('conversionMode', conversionMode)
        if copyTiePointGrids:
            node.put('copyTiePointGrids', copyTiePointGrids)
        if copyFlagBandsAndMasks:
            node.put('copyFlagBandsAndMasks', copyFlagBandsAndMasks)
        if copyNonSpectralBands:
            node.put('copyNonSpectralBands', copyNonSpectralBands)

        self.nodes.append(node)

    def add_band_pass_filter(self,
        subband = None,
        alpha: float = None
        ):
        '''
        Creates a basebanded SLC based on a subband of 1/3 the original bandwidth

        Parameters
        ----------
        subband : java.lang.String, ['low', 'high']
            Default 'low'
        alpha : double, ['0.5', '0.75', '0.8', '0.9', '1']
            Hamming alpha
            Default '1'
        '''

        node = Node('BandPassFilter')

        if subband:
            node.put('subband', subband)
        if alpha:
            node.put('alpha', alpha)

        self.nodes.append(node)

    def add_ndvi_op(self,
        redFactor: float = None,
        nirFactor: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        The retrieves the Normalized Difference Vegetation Index (NDVI).

        Parameters
        ----------
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the NDVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the NDVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('NdviOp')

        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_reip_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redB4Factor: float = None,
        redB5Factor: float = None,
        redB6Factor: float = None,
        nirFactor: float = None,
        redSourceBand4 = None,
        redSourceBand5 = None,
        redSourceBand6 = None,
        nirSourceBand = None
        ):
        '''
        The red edge inflection point index

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redB4Factor : float
            The value of the red source band (B4) is multiplied by this value.
            Default '1.0F'
        redB5Factor : float
            The value of the red source band (B5) is multiplied by this value.
            Default '1.0F'
        redB6Factor : float
            The value of the red source band (B6) is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand4 : java.lang.String
            The red band (B4) for the REIP computation. If not provided, the operator will try to find the best fitting band.
        redSourceBand5 : java.lang.String
            The red band (B5) for the REIP computation. If not provided, the operator will try to find the best fitting band.
        redSourceBand6 : java.lang.String
            The red band (B6) for the REIP computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the REIP computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('ReipOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redB4Factor:
            node.put('redB4Factor', redB4Factor)
        if redB5Factor:
            node.put('redB5Factor', redB5Factor)
        if redB6Factor:
            node.put('redB6Factor', redB6Factor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand4:
            node.put('redSourceBand4', redSourceBand4)
        if redSourceBand5:
            node.put('redSourceBand5', redSourceBand5)
        if redSourceBand6:
            node.put('redSourceBand6', redSourceBand6)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_snaphu_import(self,
        doNotKeepWrapped: bool = None
        ):
        '''
        Ingest SNAPHU results into InSAR product.

        Parameters
        ----------
        doNotKeepWrapped : boolean
            Default 'false'
        '''

        node = Node('SnaphuImport')

        if doNotKeepWrapped:
            node.put('doNotKeepWrapped', doNotKeepWrapped)

        self.nodes.append(node)

    def add_mndwi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        greenFactor: float = None,
        mirFactor: float = None,
        greenSourceBand = None,
        mirSourceBand = None
        ):
        '''
        Modified Normalized Difference Water Index, allowing for the measurement of surface water extent

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        greenFactor : float
            The value of the green source band is multiplied by this value.
            Default '1.0F'
        mirFactor : float
            The value of the MIR source band is multiplied by this value.
            Default '1.0F'
        greenSourceBand : java.lang.String
            The green band for the MNDWI computation. If not provided, the operator will try to find the best fitting band.
        mirSourceBand : java.lang.String
            The mid-infrared band for the MNDWI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('MndwiOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if greenFactor:
            node.put('greenFactor', greenFactor)
        if mirFactor:
            node.put('mirFactor', mirFactor)
        if greenSourceBand:
            node.put('greenSourceBand', greenSourceBand)
        if mirSourceBand:
            node.put('mirSourceBand', mirSourceBand)

        self.nodes.append(node)

    def add_mosaic(self,
        variables = None,
        conditions = None,
        combine = None,
        crs = None,
        orthorectify: bool = None,
        elevationModelName = None,
        resamplingName = None,
        westBound: float = None,
        northBound: float = None,
        eastBound: float = None,
        southBound: float = None,
        pixelSizeX: float = None,
        pixelSizeY: float = None
        ):
        '''
        Creates a mosaic out of a set of source products.

        Parameters
        ----------
        variables : org.esa.snap.core.gpf.common.MosaicOp$Variable[]
            Specifies the bands in the target product.
        conditions : org.esa.snap.core.gpf.common.MosaicOp$Condition[]
            Specifies valid pixels considered in the target product.
        combine : java.lang.String, ['OR', 'AND']
            Specifies the way how conditions are combined.
            Default 'OR'
        crs : java.lang.String
            The CRS of the target product, represented as WKT or authority code.
            Default 'EPSG:4326'
        orthorectify : boolean
            Whether the source product should be orthorectified.
            Default 'false'
        elevationModelName : java.lang.String
            The name of the elevation model for the orthorectification.
        resamplingName : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for resampling.
            Default 'Nearest'
        westBound : double
            The western longitude.
            Default '-15.0'
        northBound : double
            The northern latitude.
            Default '75.0'
        eastBound : double
            The eastern longitude.
            Default '30.0'
        southBound : double
            The southern latitude.
            Default '35.0'
        pixelSizeX : double
            Size of a pixel in X-direction in map units.
            Default '0.05'
        pixelSizeY : double
            Size of a pixel in Y-direction in map units.
            Default '0.05'
        '''

        node = Node('Mosaic')

        if variables:
            node.put('variables', variables)
        if conditions:
            node.put('conditions', conditions)
        if combine:
            node.put('combine', combine)
        if crs:
            node.put('crs', crs)
        if orthorectify:
            node.put('orthorectify', orthorectify)
        if elevationModelName:
            node.put('elevationModelName', elevationModelName)
        if resamplingName:
            node.put('resamplingName', resamplingName)
        if westBound:
            node.put('westBound', westBound)
        if northBound:
            node.put('northBound', northBound)
        if eastBound:
            node.put('eastBound', eastBound)
        if southBound:
            node.put('southBound', southBound)
        if pixelSizeX:
            node.put('pixelSizeX', pixelSizeX)
        if pixelSizeY:
            node.put('pixelSizeY', pixelSizeY)

        self.nodes.append(node)

    def add_stack_averaging(self,
        statistic = None
        ):
        '''
        Averaging multi-temporal images

        Parameters
        ----------
        statistic : java.lang.String, ['Mean Average', 'Minimum', 'Maximum', 'Standard Deviation', 'Coefficient of Variation']
            Default 'Mean Average'
        '''

        node = Node('Stack-Averaging')

        if statistic:
            node.put('statistic', statistic)

        self.nodes.append(node)

    def add_remove_antenna_pattern(self,
        sourceBandNames = None
        ):
        '''
        Remove Antenna Pattern

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        '''

        node = Node('RemoveAntennaPattern')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)

        self.nodes.append(node)

    def add_ipvi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        Infrared Percentage Vegetation Index retrieves the Isovegetation lines converge at origin

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the IPVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the IPVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('IpviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_meris_cloud_top_pressure_op(self,
        copyAllTiePoints: bool = None,
        straylightCorr: bool = None
        ):
        '''
        Computes cloud top pressure with FUB NN.

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        straylightCorr : boolean
            If 'true' the algorithm will apply straylight correction.
            Default 'false'
        '''

        node = Node('Meris.CloudTopPressureOp')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if straylightCorr:
            node.put('straylightCorr', straylightCorr)

        self.nodes.append(node)

    def add_dvi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        Difference Vegetation Index retrieves the Isovegetation lines parallel to soil line

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the DVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the DVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('DviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_cp_simulation(self,
        compactMode = None,
        outputFormat = None,
        noisePower: float = None,
        simulateNoiseFloor = None
        ):
        '''
        Simulation of Compact Pol data from Quad Pol data

        Parameters
        ----------
        compactMode : java.lang.String, ['Right Circular Hybrid Mode', 'Left Circular Hybrid Mode']
            The compact mode
            Default 'Right Circular Hybrid Mode'
        outputFormat : java.lang.String, ['Covariance Matrix C2', 'Scatter Vector S2']
            The output simulated compact pol data format
            Default 'Covariance Matrix C2'
        noisePower : double
            The noise power
            Default '-25'
        simulateNoiseFloor : java.lang.Boolean
            Simulate noise floor
            Default 'false'
        '''

        node = Node('CP-Simulation')

        if compactMode:
            node.put('compactMode', compactMode)
        if outputFormat:
            node.put('outputFormat', outputFormat)
        if noisePower:
            node.put('noisePower', noisePower)
        if simulateNoiseFloor:
            node.put('simulateNoiseFloor', simulateNoiseFloor)

        self.nodes.append(node)

    def add_polarimetric_decomposition(self,
        decomposition = None,
        windowSize: int = None,
        outputHAAlpha: bool = None,
        outputBetaDeltaGammaLambda: bool = None,
        outputAlpha123: bool = None,
        outputLambda123: bool = None,
        outputTouziParamSet0: bool = None,
        outputTouziParamSet1: bool = None,
        outputTouziParamSet2: bool = None,
        outputTouziParamSet3: bool = None,
        outputHuynenParamSet0: bool = None,
        outputHuynenParamSet1: bool = None
        ):
        '''
        Perform Polarimetric decomposition of a given product

        Parameters
        ----------
        decomposition : java.lang.String, ['Sinclair Decomposition', 'Pauli Decomposition', 'Freeman-Durden Decomposition', 'Generalized Freeman-Durden Decomposition', 'Yamaguchi Decomposition', 'van Zyl Decomposition', 'H-A-Alpha Quad Pol Decomposition', 'H-Alpha Dual Pol Decomposition', 'Cloude Decomposition', 'Touzi Decomposition', 'Huynen Decomposition', 'Yang Decomposition', 'Krogager Decomposition', 'Cameron Decomposition', 'Model-free 3-component Decomposition', 'Model-free 4-component Decomposition']
            Default 'Sinclair Decomposition'
        windowSize : int
            The sliding window size
            Default '5'
        outputHAAlpha : boolean
            Output entropy, anisotropy, alpha
            Default 'false'
        outputBetaDeltaGammaLambda : boolean
            Output beta, delta, gamma, lambda
            Default 'false'
        outputAlpha123 : boolean
            Output alpha 1, 2, 3
            Default 'false'
        outputLambda123 : boolean
            Output lambda 1, 2, 3
            Default 'false'
        outputTouziParamSet0 : boolean
            Output psi, tau, alpha, phi
            Default 'false'
        outputTouziParamSet1 : boolean
            Output psi1, tau1, alpha1, phi1
            Default 'false'
        outputTouziParamSet2 : boolean
            Output psi2, tau2, alpha2, phi2
            Default 'false'
        outputTouziParamSet3 : boolean
            Output psi3, tau3, alpha3, phi3
            Default 'false'
        outputHuynenParamSet0 : boolean
            Output 2A0_b, B0_plus_B, B0_minus_B
            Default 'true'
        outputHuynenParamSet1 : boolean
            Output A0, B0, B, C, D, E, F, G, H
            Default 'false'
        '''

        node = Node('Polarimetric-Decomposition')

        if decomposition:
            node.put('decomposition', decomposition)
        if windowSize:
            node.put('windowSize', windowSize)
        if outputHAAlpha:
            node.put('outputHAAlpha', outputHAAlpha)
        if outputBetaDeltaGammaLambda:
            node.put('outputBetaDeltaGammaLambda', outputBetaDeltaGammaLambda)
        if outputAlpha123:
            node.put('outputAlpha123', outputAlpha123)
        if outputLambda123:
            node.put('outputLambda123', outputLambda123)
        if outputTouziParamSet0:
            node.put('outputTouziParamSet0', outputTouziParamSet0)
        if outputTouziParamSet1:
            node.put('outputTouziParamSet1', outputTouziParamSet1)
        if outputTouziParamSet2:
            node.put('outputTouziParamSet2', outputTouziParamSet2)
        if outputTouziParamSet3:
            node.put('outputTouziParamSet3', outputTouziParamSet3)
        if outputHuynenParamSet0:
            node.put('outputHuynenParamSet0', outputHuynenParamSet0)
        if outputHuynenParamSet1:
            node.put('outputHuynenParamSet1', outputHuynenParamSet1)

        self.nodes.append(node)

    def add_add_elevation(self,
        demName = None,
        demResamplingMethod = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        elevationBandName = None
        ):
        '''
        Creates a DEM band

        Parameters
        ----------
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        demResamplingMethod : java.lang.String
            Default 'BICUBIC_INTERPOLATION'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        elevationBandName : java.lang.String
            The elevation band name.
            Default 'elevation'
        '''

        node = Node('AddElevation')

        if demName:
            node.put('demName', demName)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if elevationBandName:
            node.put('elevationBandName', elevationBandName)

        self.nodes.append(node)

    def add_goldstein_phase_filtering(self,
        alpha: float = None,
        FFTSizeString = None,
        windowSizeString = None,
        useCoherenceMask = None,
        coherenceThreshold: float = None
        ):
        '''
        Phase Filtering

        Parameters
        ----------
        alpha : double
            adaptive filter exponent
            Default '1.0'
        FFTSizeString : java.lang.String, ['32', '64', '128', '256']
            Default '64'
        windowSizeString : java.lang.String, ['3', '5', '7']
            Default '3'
        useCoherenceMask : java.lang.Boolean
            Use coherence mask
            Default 'false'
        coherenceThreshold : double
            The coherence threshold
            Default '0.2'
        '''

        node = Node('GoldsteinPhaseFiltering')

        if alpha:
            node.put('alpha', alpha)
        if FFTSizeString:
            node.put('FFTSizeString', FFTSizeString)
        if windowSizeString:
            node.put('windowSizeString', windowSizeString)
        if useCoherenceMask:
            node.put('useCoherenceMask', useCoherenceMask)
        if coherenceThreshold:
            node.put('coherenceThreshold', coherenceThreshold)

        self.nodes.append(node)

    def add_meris_smile_correction(self,
        copyAllTiePoints: bool = None
        ):
        '''
        None

        Parameters
        ----------
        copyAllTiePoints : boolean
            If set to 'false' only the lat and lon tie-points will be copied to the target product
            Default 'false'
        '''

        node = Node('Meris.SmileCorrection')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)

        self.nodes.append(node)

    def add_remote_execution_op(self,
        remoteSharedFolderPath = None,
        remoteSharedFolderUsername = None,
        remoteSharedFolderPassword = None,
        localSharedFolderPath = None,
        localPassword = None,
        slaveGraphFilePath = None,
        sourceProductFiles = None,
        remoteMachines = None,
        masterGraphFilePath = None,
        continueOnFailure = None,
        masterProductFormatName = None,
        masterProductFilePath = None,
        waitingSecondsTimeout: int = None,
        slaveProductsFolderNamePrefix = None,
        slaveProductsName = None,
        slaveProductsFormatName = None
        ):
        '''
        Executes a slave graph on a remote machine and uses the resulted products as an input for the master graph executed on the host machine.

        Parameters
        ----------
        remoteSharedFolderPath : java.lang.String
            Specifies the shared folder path.
        remoteSharedFolderUsername : java.lang.String
            Specifies the username account of the machine where the shared folder is created.
        remoteSharedFolderPassword : java.lang.String
            Specifies the password account of the machine where the shared folder is created.
        localSharedFolderPath : java.lang.String
            Specifies the local shared folder path used to connect to the remote shared folder.
        localPassword : java.lang.String
            Specifies the password of the local machine.
        slaveGraphFilePath : java.lang.String
            Specifies the slave graph file path to be executed on the remote machines.
        sourceProductFiles : java.lang.String[]
            Specifies the product files.
        remoteMachines : org.esa.snap.remote.execution.machines.RemoteMachineProperties[]
            Specifies the remote machines credentials.
        masterGraphFilePath : java.lang.String
            Specifies the master graph file path.
        continueOnFailure : java.lang.Boolean
            Specifies the flag to continue or not when a remote machine fails.
        masterProductFormatName : java.lang.String
            Specifies the master product format name.
        masterProductFilePath : java.lang.String
            Specifies the master product file path.
        waitingSecondsTimeout : int
            Specifies the waiting seconds to complete the output products on the remote machines.
        slaveProductsFolderNamePrefix : java.lang.String
            Specifies the folder name prefix of the slave output products.
        slaveProductsName : java.lang.String
            Specifies the name of the output products obtained using the slave graph.
        slaveProductsFormatName : java.lang.String
            Specifies the format name of the output products obtained using the slave graph.
        '''

        node = Node('RemoteExecutionOp')

        if remoteSharedFolderPath:
            node.put('remoteSharedFolderPath', remoteSharedFolderPath)
        if remoteSharedFolderUsername:
            node.put('remoteSharedFolderUsername', remoteSharedFolderUsername)
        if remoteSharedFolderPassword:
            node.put('remoteSharedFolderPassword', remoteSharedFolderPassword)
        if localSharedFolderPath:
            node.put('localSharedFolderPath', localSharedFolderPath)
        if localPassword:
            node.put('localPassword', localPassword)
        if slaveGraphFilePath:
            node.put('slaveGraphFilePath', slaveGraphFilePath)
        if sourceProductFiles:
            node.put('sourceProductFiles', sourceProductFiles)
        if remoteMachines:
            node.put('remoteMachines', remoteMachines)
        if masterGraphFilePath:
            node.put('masterGraphFilePath', masterGraphFilePath)
        if continueOnFailure:
            node.put('continueOnFailure', continueOnFailure)
        if masterProductFormatName:
            node.put('masterProductFormatName', masterProductFormatName)
        if masterProductFilePath:
            node.put('masterProductFilePath', masterProductFilePath)
        if waitingSecondsTimeout:
            node.put('waitingSecondsTimeout', waitingSecondsTimeout)
        if slaveProductsFolderNamePrefix:
            node.put('slaveProductsFolderNamePrefix', slaveProductsFolderNamePrefix)
        if slaveProductsName:
            node.put('slaveProductsName', slaveProductsName)
        if slaveProductsFormatName:
            node.put('slaveProductsFormatName', slaveProductsFormatName)

        self.nodes.append(node)

    def add_polarimetric_speckle_filter(self,
        filter = None,
        filterSize: int = None,
        numLooksStr = None,
        windowSize = None,
        targetWindowSizeStr = None,
        anSize: int = None,
        sigmaStr = None,
        searchWindowSizeStr = None,
        patchSizeStr = None,
        scaleSizeStr = None
        ):
        '''
        Polarimetric Speckle Reduction

        Parameters
        ----------
        filter : java.lang.String, ['Box Car Filter', 'IDAN Filter', 'Refined Lee Filter', 'Improved Lee Sigma Filter']
            Default 'Refined Lee Filter'
        filterSize : int
            The filter size
            Default '5'
        numLooksStr : java.lang.String, ['1', '2', '3', '4']
            Default '1'
        windowSize : java.lang.String, ['5x5', '7x7', '9x9', '11x11', '13x13', '15x15', '17x17']
            Default '7x7'
        targetWindowSizeStr : java.lang.String, ['3x3', '5x5']
            Default '3x3'
        anSize : int
            The Adaptive Neighbourhood size
            Default '50'
        sigmaStr : java.lang.String, ['0.5', '0.6', '0.7', '0.8', '0.9']
            Default '0.9'
        searchWindowSizeStr : java.lang.String, ['3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25']
            The search window size
            Default '15'
        patchSizeStr : java.lang.String, ['3', '5', '7', '9', '11']
            The patch size
            Default '5'
        scaleSizeStr : java.lang.String, ['0', '1', '2']
            The scale size
            Default '1'
        '''

        node = Node('Polarimetric-Speckle-Filter')

        if filter:
            node.put('filter', filter)
        if filterSize:
            node.put('filterSize', filterSize)
        if numLooksStr:
            node.put('numLooksStr', numLooksStr)
        if windowSize:
            node.put('windowSize', windowSize)
        if targetWindowSizeStr:
            node.put('targetWindowSizeStr', targetWindowSizeStr)
        if anSize:
            node.put('anSize', anSize)
        if sigmaStr:
            node.put('sigmaStr', sigmaStr)
        if searchWindowSizeStr:
            node.put('searchWindowSizeStr', searchWindowSizeStr)
        if patchSizeStr:
            node.put('patchSizeStr', patchSizeStr)
        if scaleSizeStr:
            node.put('scaleSizeStr', scaleSizeStr)

        self.nodes.append(node)

    def add_grd_post(self
        ):
        '''
        Applies GRD post-processing

        Parameters
        ----------
        '''

        node = Node('GRD-Post')


        self.nodes.append(node)

    def add_iem_multi_angle_inversion(self,
        N = None,
        M = None,
        doRemainingOutliersFilter = None,
        lutFile = None,
        sigmaPol = None,
        outputRMS = None,
        thresholdRDC = None
        ):
        '''
        Performs IEM inversion using Multi-angle approach

        Parameters
        ----------
        N : java.lang.Integer
            # closest sigma match from LUT search
            Default '5'
        M : java.lang.Integer
            Length (pixels) of side of square neighbourhood (M)
            Default '5'
        doRemainingOutliersFilter : java.lang.Boolean
            Replace remaining outlier with neighbours's average
            Default 'true'
        lutFile : java.io.File
        sigmaPol : java.lang.String, ['HH1-HH2', 'HH1-VV2', 'VV1-VV2', 'VV1-HH2']
            Multi-Angle Polarizations
            Default 'HH1-HH2'
        outputRMS : java.lang.Boolean
            Optional rms in output
            Default 'false'
        thresholdRDC : java.lang.Double
            RDC deviation threshold
            Default '0.5'
        '''

        node = Node('IEM-Multi-Angle-Inversion')

        if N:
            node.put('N', N)
        if M:
            node.put('M', M)
        if doRemainingOutliersFilter:
            node.put('doRemainingOutliersFilter', doRemainingOutliersFilter)
        if lutFile:
            node.put('lutFile', lutFile)
        if sigmaPol:
            node.put('sigmaPol', sigmaPol)
        if outputRMS:
            node.put('outputRMS', outputRMS)
        if thresholdRDC:
            node.put('thresholdRDC', thresholdRDC)

        self.nodes.append(node)

    def add_change_vector_analysis_op(self,
        sourceBand1 = None,
        sourceBand2 = None,
        magnitudeThreshold = None
        ):
        '''
        The 'Change Vector Analysis' between two dual bands at two differents dates.

        Parameters
        ----------
        sourceBand1 : java.lang.String
            Band 1 at the same date
        sourceBand2 : java.lang.String
            Band 2 at the same date
        magnitudeThreshold : java.lang.String
            No change detection magnitude threshold
            Default '0'
        '''

        node = Node('ChangeVectorAnalysisOp')

        if sourceBand1:
            node.put('sourceBand1', sourceBand1)
        if sourceBand2:
            node.put('sourceBand2', sourceBand2)
        if magnitudeThreshold:
            node.put('magnitudeThreshold', magnitudeThreshold)

        self.nodes.append(node)

    def add_compactpol_radar_vegetation_index(self,
        windowSize: int = None
        ):
        '''
        Compact-pol Radar Vegetation Indices generation

        Parameters
        ----------
        windowSize : int
            The sliding window size
            Default '5'
        '''

        node = Node('Compactpol-Radar-Vegetation-Index')

        if windowSize:
            node.put('windowSize', windowSize)

        self.nodes.append(node)

    def add_topsar_merge(self,
        selectedPolarisations = None
        ):
        '''
        Merge subswaths of a Sentinel-1 TOPSAR product

        Parameters
        ----------
        selectedPolarisations : java.lang.String[]
            The list of polarisations
        '''

        node = Node('TOPSAR-Merge')

        if selectedPolarisations:
            node.put('selectedPolarisations', selectedPolarisations)

        self.nodes.append(node)

    def add_maximum_likelihood_classifier(self,
        numTrainSamples: int = None,
        savedClassifierName = None,
        doLoadClassifier = None,
        doClassValQuantization = None,
        minClassValue = None,
        classValStepSize = None,
        classLevels: int = None,
        trainOnRaster = None,
        trainingBands = None,
        trainingVectors = None,
        featureBands = None,
        labelSource = None,
        evaluateClassifier = None,
        evaluateFeaturePowerSet = None,
        minPowerSetSize = None,
        maxPowerSetSize = None
        ):
        '''
        Maximum Likelihood classifier

        Parameters
        ----------
        numTrainSamples : int
            The number of training samples
            Default '5000'
        savedClassifierName : java.lang.String
            The saved classifier name
        doLoadClassifier : java.lang.Boolean
            Choose to save or load classifier
            Default 'false'
        doClassValQuantization : java.lang.Boolean
            Quantization for raster training
            Default 'true'
        minClassValue : java.lang.Double
            Quantization min class value for raster training
            Default '0.0'
        classValStepSize : java.lang.Double
            Quantization step size for raster training
            Default '5.0'
        classLevels : int
            Quantization class levels for raster training
            Default '101'
        trainOnRaster : java.lang.Boolean
            Train on raster or vector data
            Default 'true'
        trainingBands : java.lang.String[]
            Raster bands to train on
        trainingVectors : java.lang.String[]
            Vectors to train on
        featureBands : java.lang.String[]
            Names of bands to be used as features
        labelSource : java.lang.String
            'VectorNodeName' or specific Attribute name
        evaluateClassifier : java.lang.Boolean
            Evaluate classifier and features
        evaluateFeaturePowerSet : java.lang.Boolean
            Evaluate the power set of features
            Default 'false'
        minPowerSetSize : java.lang.Integer
            Minimum size of the power set of features
            Default '2'
        maxPowerSetSize : java.lang.Integer
            Maximum size of the power set of features
            Default '7'
        '''

        node = Node('Maximum-Likelihood-Classifier')

        if numTrainSamples:
            node.put('numTrainSamples', numTrainSamples)
        if savedClassifierName:
            node.put('savedClassifierName', savedClassifierName)
        if doLoadClassifier:
            node.put('doLoadClassifier', doLoadClassifier)
        if doClassValQuantization:
            node.put('doClassValQuantization', doClassValQuantization)
        if minClassValue:
            node.put('minClassValue', minClassValue)
        if classValStepSize:
            node.put('classValStepSize', classValStepSize)
        if classLevels:
            node.put('classLevels', classLevels)
        if trainOnRaster:
            node.put('trainOnRaster', trainOnRaster)
        if trainingBands:
            node.put('trainingBands', trainingBands)
        if trainingVectors:
            node.put('trainingVectors', trainingVectors)
        if featureBands:
            node.put('featureBands', featureBands)
        if labelSource:
            node.put('labelSource', labelSource)
        if evaluateClassifier:
            node.put('evaluateClassifier', evaluateClassifier)
        if evaluateFeaturePowerSet:
            node.put('evaluateFeaturePowerSet', evaluateFeaturePowerSet)
        if minPowerSetSize:
            node.put('minPowerSetSize', minPowerSetSize)
        if maxPowerSetSize:
            node.put('maxPowerSetSize', maxPowerSetSize)

        self.nodes.append(node)

    def add_polarimetric_matrices(self,
        matrix = None
        ):
        '''
        Generates covariance or coherency matrix for given product

        Parameters
        ----------
        matrix : java.lang.String, ['C2', 'C3', 'C4', 'T3', 'T4']
            The covariance or coherency matrix
            Default 'T3'
        '''

        node = Node('Polarimetric-Matrices')

        if matrix:
            node.put('matrix', matrix)

        self.nodes.append(node)

    def add_rvi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        Ratio Vegetation Index retrieves the Isovegetation lines converge at origin

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        redSourceBand : java.lang.String
            The red band for the RVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the RVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('RviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_cross_resampling(self,
        warpPolynomialOrder: int = None,
        interpolationMethod = None,
        targetGeometry = None
        ):
        '''
        Estimate Resampling Polynomial using SAR Image Geometry, and Resample Input Images

        Parameters
        ----------
        warpPolynomialOrder : int, ['1', '2', '3']
            The order of polynomial function
            Default '2'
        interpolationMethod : java.lang.String, ['Cubic convolution (4 points)', 'Cubic convolution (6 points)', 'Truncated sinc (6 points)', 'Truncated sinc (8 points)', 'Truncated sinc (16 points)']
            Default 'Cubic convolution (6 points)'
        targetGeometry : java.lang.String, ['ERS', 'Envisat ASAR']
            Default 'ERS'
        '''

        node = Node('CrossResampling')

        if warpPolynomialOrder:
            node.put('warpPolynomialOrder', warpPolynomialOrder)
        if interpolationMethod:
            node.put('interpolationMethod', interpolationMethod)
        if targetGeometry:
            node.put('targetGeometry', targetGeometry)

        self.nodes.append(node)

    def add_iem_hybrid_inversion(self,
        N = None,
        M = None,
        doRemainingOutliersFilter = None,
        lutFile = None,
        outputRMS = None,
        outputCL = None,
        thresholdRDC = None
        ):
        '''
        Performs IEM inversion using Hybrid approach

        Parameters
        ----------
        N : java.lang.Integer
            # closest sigma match from LUT search
            Default '5'
        M : java.lang.Integer
            Length (pixels) of side of square neighbourhood (M)
            Default '5'
        doRemainingOutliersFilter : java.lang.Boolean
            Replace remaining outlier with neighbours's average
            Default 'true'
        lutFile : java.io.File
        outputRMS : java.lang.Boolean
            Optional rms in output
            Default 'false'
        outputCL : java.lang.Boolean
            Optional cl in output
            Default 'false'
        thresholdRDC : java.lang.Double
            RDC deviation threshold
            Default '0.5'
        '''

        node = Node('IEM-Hybrid-Inversion')

        if N:
            node.put('N', N)
        if M:
            node.put('M', M)
        if doRemainingOutliersFilter:
            node.put('doRemainingOutliersFilter', doRemainingOutliersFilter)
        if lutFile:
            node.put('lutFile', lutFile)
        if outputRMS:
            node.put('outputRMS', outputRMS)
        if outputCL:
            node.put('outputCL', outputCL)
        if thresholdRDC:
            node.put('thresholdRDC', thresholdRDC)

        self.nodes.append(node)

    def add_cp_decomposition(self,
        decomposition = None,
        windowSizeXStr = None,
        windowSizeYStr = None,
        computeAlphaByT3: bool = None,
        outputRVOG: bool = None
        ):
        '''
        Perform Compact Polarimetric decomposition of a given product

        Parameters
        ----------
        decomposition : java.lang.String, ['M-Chi Decomposition', 'M-Delta Decomposition', 'H-Alpha Decomposition', '2 Layer RVOG Model Based Decomposition', 'Model-free 3-component decomposition']
            Default 'M-Chi Decomposition'
        windowSizeXStr : java.lang.String, ['3', '5', '7', '9', '11', '13', '15', '17', '19']
            Default '5'
        windowSizeYStr : java.lang.String, ['3', '5', '7', '9', '11', '13', '15', '17', '19']
            Default '5'
        computeAlphaByT3 : boolean
            Compute alpha by coherency matrix T3
            Default 'true'
        outputRVOG : boolean
            Output RVOG parameters mv, ms, alphaS and phi
            Default 'true'
        '''

        node = Node('CP-Decomposition')

        if decomposition:
            node.put('decomposition', decomposition)
        if windowSizeXStr:
            node.put('windowSizeXStr', windowSizeXStr)
        if windowSizeYStr:
            node.put('windowSizeYStr', windowSizeYStr)
        if computeAlphaByT3:
            node.put('computeAlphaByT3', computeAlphaByT3)
        if outputRVOG:
            node.put('outputRVOG', outputRVOG)

        self.nodes.append(node)

    def add_create_stack(self,
        masterBandNames = None,
        slaveBandNames = None,
        resamplingType = None,
        extent = None,
        initialOffsetMethod = None
        ):
        '''
        Collocates two or more products based on their geo-codings.

        Parameters
        ----------
        masterBandNames : java.lang.String[]
            The list of source bands.
        slaveBandNames : java.lang.String[]
            The list of source bands.
        resamplingType : java.lang.String
            The method to be used when resampling the slave grid onto the master grid.
            Default 'NONE'
        extent : java.lang.String, ['Master', 'Minimum', 'Maximum']
            The output image extents.
            Default 'Master'
        initialOffsetMethod : java.lang.String, ['Orbit', 'Product Geolocation']
            Method for computing initial offset between master and slave
            Default 'Orbit'
        '''

        node = Node('CreateStack')

        if masterBandNames:
            node.put('masterBandNames', masterBandNames)
        if slaveBandNames:
            node.put('slaveBandNames', slaveBandNames)
        if resamplingType:
            node.put('resamplingType', resamplingType)
        if extent:
            node.put('extent', extent)
        if initialOffsetMethod:
            node.put('initialOffsetMethod', initialOffsetMethod)

        self.nodes.append(node)

    def add_multilook(self,
        sourceBandNames = None,
        nRgLooks: int = None,
        nAzLooks: int = None,
        outputIntensity = None,
        grSquarePixel = None
        ):
        '''
        Averages the power across a number of lines in both the azimuth and range directions

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        nRgLooks : int
            The user defined number of range looks
            Default '1'
        nAzLooks : int
            The user defined number of azimuth looks
            Default '1'
        outputIntensity : java.lang.Boolean
            For complex product output intensity or i and q
            Default 'false'
        grSquarePixel : java.lang.Boolean
            Use ground square pixel
            Default 'true'
        '''

        node = Node('Multilook')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if nRgLooks:
            node.put('nRgLooks', nRgLooks)
        if nAzLooks:
            node.put('nAzLooks', nAzLooks)
        if outputIntensity:
            node.put('outputIntensity', outputIntensity)
        if grSquarePixel:
            node.put('grSquarePixel', grSquarePixel)

        self.nodes.append(node)

    def add_back_geocoding(self,
        demName = None,
        demResamplingMethod = None,
        externalDEMFile = None,
        externalDEMNoDataValue: float = None,
        resamplingType = None,
        maskOutAreaWithoutElevation: bool = None,
        outputRangeAzimuthOffset: bool = None,
        outputDerampDemodPhase: bool = None,
        disableReramp: bool = None
        ):
        '''
        Bursts co-registration using orbit and DEM

        Parameters
        ----------
        demName : java.lang.String
            The digital elevation model.
            Default 'SRTM 3Sec'
        demResamplingMethod : java.lang.String
            Default 'BICUBIC_INTERPOLATION'
        externalDEMFile : java.io.File
        externalDEMNoDataValue : double
            Default '0'
        resamplingType : java.lang.String
            The method to be used when resampling the slave grid onto the master grid.
            Default 'BISINC_5_POINT_INTERPOLATION'
        maskOutAreaWithoutElevation : boolean
            Default 'true'
        outputRangeAzimuthOffset : boolean
            Default 'false'
        outputDerampDemodPhase : boolean
            Default 'false'
        disableReramp : boolean
            Default 'false'
        '''

        node = Node('Back-Geocoding')

        if demName:
            node.put('demName', demName)
        if demResamplingMethod:
            node.put('demResamplingMethod', demResamplingMethod)
        if externalDEMFile:
            node.put('externalDEMFile', externalDEMFile)
        if externalDEMNoDataValue:
            node.put('externalDEMNoDataValue', externalDEMNoDataValue)
        if resamplingType:
            node.put('resamplingType', resamplingType)
        if maskOutAreaWithoutElevation:
            node.put('maskOutAreaWithoutElevation', maskOutAreaWithoutElevation)
        if outputRangeAzimuthOffset:
            node.put('outputRangeAzimuthOffset', outputRangeAzimuthOffset)
        if outputDerampDemodPhase:
            node.put('outputDerampDemodPhase', outputDerampDemodPhase)
        if disableReramp:
            node.put('disableReramp', disableReramp)

        self.nodes.append(node)

    def add_replace_metadata(self,
        note = None
        ):
        '''
        Replace the metadata of the first product with that of the second

        Parameters
        ----------
        note : java.lang.String
            Default 'Replace the metadata of the first product with that of the second'
        '''

        node = Node('ReplaceMetadata')

        if note:
            node.put('note', note)

        self.nodes.append(node)

    def add_pvi_op(self,
        resampleType = None,
        upsamplingMethod = None,
        downsamplingMethod = None,
        redFactor: float = None,
        nirFactor: float = None,
        angleSoilLineNIRAxis: float = None,
        redSourceBand = None,
        nirSourceBand = None
        ):
        '''
        Perpendicular Vegetation Index retrieves the Isovegetation lines parallel to soil line.
Soil line has an arbitrary slope and passes through origin

        Parameters
        ----------
        resampleType : java.lang.String, ['None', 'Lowest resolution', 'Highest resolution']
            If selected band s differ in size, the resample method used before computing the index
            Default 'None'
        upsamplingMethod : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for interpolation (upsampling to a finer resolution).
            Default 'Nearest'
        downsamplingMethod : java.lang.String, ['First', 'Min', 'Max', 'Mean', 'Median']
            The method used for aggregation (downsampling to a coarser resolution).
            Default 'First'
        redFactor : float
            The value of the red source band is multiplied by this value.
            Default '1.0F'
        nirFactor : float
            The value of the NIR source band is multiplied by this value.
            Default '1.0F'
        angleSoilLineNIRAxis : float
            Soil line has an arbitrary slope and passes through origin.
            Default '45.0'
        redSourceBand : java.lang.String
            The red band for the PVI computation. If not provided, the operator will try to find the best fitting band.
        nirSourceBand : java.lang.String
            The near-infrared band for the PVI computation. If not provided, the operator will try to find the best fitting band.
        '''

        node = Node('PviOp')

        if resampleType:
            node.put('resampleType', resampleType)
        if upsamplingMethod:
            node.put('upsamplingMethod', upsamplingMethod)
        if downsamplingMethod:
            node.put('downsamplingMethod', downsamplingMethod)
        if redFactor:
            node.put('redFactor', redFactor)
        if nirFactor:
            node.put('nirFactor', nirFactor)
        if angleSoilLineNIRAxis:
            node.put('angleSoilLineNIRAxis', angleSoilLineNIRAxis)
        if redSourceBand:
            node.put('redSourceBand', redSourceBand)
        if nirSourceBand:
            node.put('nirSourceBand', nirSourceBand)

        self.nodes.append(node)

    def add_forest_area_classification(self,
        sourceBandNames = None,
        numClasses: int = None,
        maxIterations: int = None,
        convergenceThreshold: int = None
        ):
        '''
        Detect forest area

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            The list of source bands.
        numClasses : int
            The number of classes
            Default '3'
        maxIterations : int
            The maximum number of iterations
            Default '10'
        convergenceThreshold : int
            The convergence threshold
            Default '95'
        '''

        node = Node('Forest-Area-Classification')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if numClasses:
            node.put('numClasses', numClasses)
        if maxIterations:
            node.put('maxIterations', maxIterations)
        if convergenceThreshold:
            node.put('convergenceThreshold', convergenceThreshold)

        self.nodes.append(node)

    def add_dark_object_subtraction(self,
        sourceBandNames = None,
        maskExpression = None,
        histogramMinimumPercentile: int = None
        ):
        '''
        Performs dark object subtraction for spectral bands in source product.

        Parameters
        ----------
        sourceBandNames : java.lang.String[]
            Bands to be copied to the target. DOS will be applied on spectral bands only.
        maskExpression : java.lang.String
            Mask expression defining search area for dark object.
        histogramMinimumPercentile : int, ['0', '1', '5']
            Percentile of minimum in image data in percent (the number means how many percent of the image data are lower than detected minimum.
        '''

        node = Node('DarkObjectSubtraction')

        if sourceBandNames:
            node.put('sourceBandNames', sourceBandNames)
        if maskExpression:
            node.put('maskExpression', maskExpression)
        if histogramMinimumPercentile:
            node.put('histogramMinimumPercentile', histogramMinimumPercentile)

        self.nodes.append(node)

    def add_temporal_percentile(self,
        sourceProductPaths = None,
        startDate = None,
        endDate = None,
        keepIntermediateTimeSeriesProduct: bool = None,
        timeSeriesOutputDir = None,
        crs = None,
        resamplingMethodName = None,
        westBound: float = None,
        northBound: float = None,
        eastBound: float = None,
        southBound: float = None,
        pixelSizeX: float = None,
        pixelSizeY: float = None,
        sourceBandName = None,
        bandMathsExpression = None,
        percentileBandNamePrefix = None,
        validPixelExpression = None,
        percentiles = None,
        gapFillingMethod = None,
        startValueFallback = None,
        endValueFallback = None
        ):
        '''
        Computes percentiles over a given time period.

        Parameters
        ----------
        sourceProductPaths : java.lang.String[]
            A comma-separated list of file paths specifying the source products.
            Source products to be considered for percentile computation. 
            Each path may contain the wildcards '**' (matches recursively any directory),
            '*' (matches any character sequence in path names) and
            '?' (matches any single character).
            If, for example, all NetCDF files under /eodata/ shall be considered, use '/eodata/**/*.nc'.
        startDate : org.esa.snap.core.datamodel.ProductData$UTC
            The start date. If not given, it is taken from the 'oldest' source product. Products that
            have a start date earlier than the start date given by this parameter are not considered.
        endDate : org.esa.snap.core.datamodel.ProductData$UTC
            The end date. If not given, it is taken from the 'newest' source product. Products that
            have an end date later than the end date given by this parameter are not considered.
        keepIntermediateTimeSeriesProduct : boolean
            Determines whether the time series product which is created during computation
            should be written to disk.
            Default 'true'
        timeSeriesOutputDir : java.io.File
            The output directory for the intermediate time series product. If not given, the time
            series product will be written to the working directory.
        crs : java.lang.String
            A text specifying the target Coordinate Reference System, either in WKT or as an
            authority code. For appropriate EPSG authority codes see (www.epsg-registry.org).
            AUTO authority can be used with code 42001 (UTM), and 42002 (Transverse Mercator)
            where the scene center is used as reference. Examples: EPSG:4326, AUTO:42001
            Default 'EPSG:4326'
        resamplingMethodName : java.lang.String, ['Nearest', 'Bilinear', 'Bicubic']
            The method used for resampling of floating-point raster data, if source products must
            be reprojected to the target CRS.
            Default 'Nearest'
        westBound : double
            The most-western longitude. All values west of this longitude will not be considered.
            Default '-15.0'
        northBound : double
            The most-northern latitude. All values north of this latitude will not be considered.
            Default '75.0'
        eastBound : double
            The most-eastern longitude. All values east of this longitude will not be considered.
            Default '30.0'
        southBound : double
            The most-southern latitude. All values south of this latitude will not be considered.
            Default '35.0'
        pixelSizeX : double
            Size of a pixel in X-direction in map units.
            Default '0.05'
        pixelSizeY : double
            Size of a pixel in Y-direction in map units.
            Default '0.05'
        sourceBandName : java.lang.String
            The name of the band in the source products. Either this or 'bandMathsExpression' must be provided.
        bandMathsExpression : java.lang.String
            A band maths expression serving as input band. Either this or 'sourceBandName' must be provided.
        percentileBandNamePrefix : java.lang.String
            If given, this is the percentile band name prefix. If empty, the resulting percentile band’s name
            prefix will be either the 'sourceBandName' or created from the 'bandMathsExpression'.
        validPixelExpression : java.lang.String
            The valid pixel expression serving as criterion for whether to consider pixels for computation.
            Default 'true'
        percentiles : int[]
            The percentiles.
            Default '90'
        gapFillingMethod : java.lang.String, ['noGapFilling', 'gapFillingLinearInterpolation', 'gapFillingSplineInterpolation', 'gapFillingQuadraticInterpolation']
            The gap filling method for percentile calculation.
            Default 'gapFillingLinearInterpolation'
        startValueFallback : java.lang.Double
            The fallback value for the start of a pixel time series. It will be considered if
            there is no valid value at the pixel of the oldest collocated mean band. This would be
            the case, if, e.g., there is a cloudy day at the time period start.
            Default '0.0'
        endValueFallback : java.lang.Double
            The fallback value for the end of a pixel time series. It will be considered ifthere is no valid value at the pixel of the newest collocated mean band. This would be
            the case, if, e.g., there is a cloudy day at the time period end.
            Default '0.0'
        '''

        node = Node('TemporalPercentile')

        if sourceProductPaths:
            node.put('sourceProductPaths', sourceProductPaths)
        if startDate:
            node.put('startDate', startDate)
        if endDate:
            node.put('endDate', endDate)
        if keepIntermediateTimeSeriesProduct:
            node.put('keepIntermediateTimeSeriesProduct', keepIntermediateTimeSeriesProduct)
        if timeSeriesOutputDir:
            node.put('timeSeriesOutputDir', timeSeriesOutputDir)
        if crs:
            node.put('crs', crs)
        if resamplingMethodName:
            node.put('resamplingMethodName', resamplingMethodName)
        if westBound:
            node.put('westBound', westBound)
        if northBound:
            node.put('northBound', northBound)
        if eastBound:
            node.put('eastBound', eastBound)
        if southBound:
            node.put('southBound', southBound)
        if pixelSizeX:
            node.put('pixelSizeX', pixelSizeX)
        if pixelSizeY:
            node.put('pixelSizeY', pixelSizeY)
        if sourceBandName:
            node.put('sourceBandName', sourceBandName)
        if bandMathsExpression:
            node.put('bandMathsExpression', bandMathsExpression)
        if percentileBandNamePrefix:
            node.put('percentileBandNamePrefix', percentileBandNamePrefix)
        if validPixelExpression:
            node.put('validPixelExpression', validPixelExpression)
        if percentiles:
            node.put('percentiles', percentiles)
        if gapFillingMethod:
            node.put('gapFillingMethod', gapFillingMethod)
        if startValueFallback:
            node.put('startValueFallback', startValueFallback)
        if endValueFallback:
            node.put('endValueFallback', endValueFallback)

        self.nodes.append(node)

    def add_meris_brr(self,
        copyAllTiePoints: bool = None,
        copyL1Flags: bool = None,
        outputToar: bool = None,
        correctionSurface = None
        ):
        '''
        Performs the Rayleigh correction on a MERIS L1b product.

        Parameters
        ----------
        copyAllTiePoints : boolean
            Write all tie points to the target product
            Default 'true'
        copyL1Flags : boolean
            Write L1 flags to the target product.
            Default 'true'
        outputToar : boolean
            Write TOA reflectances to the target product.
            Default 'false'
        correctionSurface : org.esa.s3tbx.meris.brr.operator.CorrectionSurfaceEnum, ['ALL_SURFACES', 'LAND', 'WATER']
            Specify the surface where the Rayleigh correction shall be performed
            Default 'ALL_SURFACES'
        '''

        node = Node('Meris.Brr')

        if copyAllTiePoints:
            node.put('copyAllTiePoints', copyAllTiePoints)
        if copyL1Flags:
            node.put('copyL1Flags', copyL1Flags)
        if outputToar:
            node.put('outputToar', outputToar)
        if correctionSurface:
            node.put('correctionSurface', correctionSurface)

        self.nodes.append(node)

    def add_land_water_mask(self,
        resolution: int = None,
        subSamplingFactorX: int = None,
        subSamplingFactorY: int = None
        ):
        '''
        Operator creating a target product with a single band containing a land/water-mask.

        Parameters
        ----------
        resolution : int, ['50', '150', '1000']
            Specifies on which resolution the water mask shall be based.
            Default '50'
        subSamplingFactorX : int
            Specifies the factor between the resolution of the source product and the watermask in x direction. A value of '1' means no subsampling at all.
            Default '1'
        subSamplingFactorY : int
            Specifies the factor between the resolution of the source product and the watermask iny direction. A value of '1' means no subsampling at all.
            Default '1'
        '''

        node = Node('LandWaterMask')

        if resolution:
            node.put('resolution', resolution)
        if subSamplingFactorX:
            node.put('subSamplingFactorX', subSamplingFactorX)
        if subSamplingFactorY:
            node.put('subSamplingFactorY', subSamplingFactorY)

        self.nodes.append(node)

