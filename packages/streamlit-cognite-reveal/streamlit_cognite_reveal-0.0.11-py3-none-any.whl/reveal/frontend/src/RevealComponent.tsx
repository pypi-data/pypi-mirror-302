import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode, useEffect, useMemo, useState } from "react"
import {
  RevealCanvas,
  AxisGizmo,
  RevealContext,
  SceneContainer,
  useClickedNodeData,
  RevealToolbar,
  AssetStylingGroup,
  useSceneDefaultCamera,
  useReveal,
  use3dModels,
} from "@cognite/reveal-react-components"
import * as THREE from 'three'
import { CogniteClient } from "@cognite/sdk"
import { CogniteCadModel, DefaultNodeAppearance, NodeAppearance, PropertyFilterNodeCollection } from "@cognite/reveal"
import {getNodeAppearanceFromString, getClippingPlanesFromArgs, toCamelCase} from "./apiUtils"

interface StState {
  boundingBoxMin?: number[]
  boundingBoxMax?: number[]
  lastClickedAsset: number | null
}

interface StClientConfig {
  // TODO: fix a way to call back to Python to generate a new token
  token: string
  project: string
  baseUrl: string
}

const ClippingPlanes = ({planes}: {planes: THREE.Plane[]}) => {
  const viewer = useReveal();
  viewer.setGlobalClippingPlanes(planes);
  return <></>
}

// The StateComponent is responsible for managing the state of the Reveal component.
const StateComponent = ({sceneExternalId, sceneSpace, selectedAssetIdsArg, defaultAppearance}: {
  sceneExternalId: string, 
  sceneSpace: string, 
  selectedAssetIdsArg: number[],
  defaultAppearance?: NodeAppearance
}) => {
  const defaultAssetStyling: AssetStylingGroup = {
    assetIds: [],
    style: {
      cad: DefaultNodeAppearance.Highlighted
    }
  };

  const [styling, setStyling] = useState<AssetStylingGroup>(defaultAssetStyling);
  const [selectedAssetIds, setSelectedAssetIds] = useState(selectedAssetIdsArg)
  const [modelBoundingBox, setModelBoundingBox] = useState<THREE.Box3 | null>(null)

  const models = use3dModels();

  useEffect(() => {
    // Read model information and store in state
    (async () => {
      for (let i = 0; i < models.length; i++) {
        // Todo: handle multiple models
        let model = models[i]
        if (model instanceof CogniteCadModel) {
          const modelBoundingBox = await model.getModelBoundingBox();
          setModelBoundingBox(modelBoundingBox);
        }
      }
    })()
    
  }, [models])
  
  useEffect(() => {
    setSelectedAssetIds(selectedAssetIdsArg)
  }, [selectedAssetIdsArg])
  
  useEffect(() => {
    const assetStyling: AssetStylingGroup = {
      assetIds: selectedAssetIds,
      style: {
        cad: DefaultNodeAppearance.Highlighted
      }
    };
    setStyling(assetStyling)
  }, [selectedAssetIds])

  const [lastClickedAsset, setLastClickedAsset] = useState<number | null>(null);
  useMemo(() => {
    const boundingBoxMax = modelBoundingBox?.max.toArray();
    const boundingBoxMin = modelBoundingBox?.min.toArray();
    
    // TODO: For some reason, setting the bounding boxes
    // causes streamlit to hang. Maybe it causes infinite rendering?
    const state: StState = { lastClickedAsset, boundingBoxMin, boundingBoxMax};
    console.log('state: ', state);
    Streamlit.setComponentValue(state);
  }, [lastClickedAsset, modelBoundingBox])
  
  return <>
    <SceneContainer
      sceneExternalId={sceneExternalId}
      sceneSpaceId={sceneSpace}
      // instanceStyling={[styling]}
      defaultResourceStyling={
        {
          cad: {
            default: defaultAppearance,
          }
        }
      }
    />
    <AssetClickedHandler setLastClickedAsset={setLastClickedAsset} />
  </>
}

const ApplyStyledNodeCollections = ({styledNodeCollections, sdk}: {styledNodeCollections: any[], sdk: CogniteClient}) => {
  const models = use3dModels();

  useEffect(() => {
    models.forEach(model => {
      
      // This only applies to CogniteCadModel instances
      if (model instanceof CogniteCadModel) {
        // Now loop over all styled node collections and apply them
        styledNodeCollections.forEach(async styledNodeCollection => {
          const nodeFilter = new PropertyFilterNodeCollection(sdk, model);
          await nodeFilter.executeFilter(styledNodeCollection.filter_criteria);
          
          // Extract only non-null values from styledNodeCollection.node_appearance
          // and convert to camelCase.
          const nodeAppearance = Object.fromEntries(
            Object.entries(styledNodeCollection.node_appearance)
              .filter(([key, value]) => value !== null)
              .map(([key, value]) => [toCamelCase(key), value])
          );

          // Look for key 'color' and special handle it.
          // Either we have an array of 3 numbers or a string with a color name.
          if (nodeAppearance['color']) {
            const color = nodeAppearance['color'];
            if (Array.isArray(color) && color.length === 3) {
              nodeAppearance['color'] = new THREE.Color(color[0], color[1], color[2]);
            } else if (typeof color === 'string') {
              nodeAppearance['color'] = new THREE.Color(color);
            }
          }
          for (let i = model.styledNodeCollections.length - 1; i >= 0; i--) {
            const viewerStyledNodeCollection = model.styledNodeCollections[i];
            model.unassignStyledNodeCollection(viewerStyledNodeCollection.nodeCollection);
          }
          model.assignStyledNodeCollection(nodeFilter, nodeAppearance);
        })
      }
    })
  }, [styledNodeCollections, sdk, models])
  return <></>
}

const AssetClickedHandler = ({setLastClickedAsset}: { setLastClickedAsset: (assetId: number) => void}) => {
  const clicked = useClickedNodeData();
  useEffect(() => {
    if (clicked && clicked.assetMappingResult && clicked.assetMappingResult.assetIds.length > 0) {
      setLastClickedAsset(clicked.assetMappingResult.assetIds[0]);
    }  
  }, [clicked, setLastClickedAsset]);
  return <></>
};

const LoadDefaultCamera =  ({sceneExternalId, sceneSpace}: {sceneExternalId: string; sceneSpace: string}) => {
  const loadDefaultCamera = useSceneDefaultCamera(sceneExternalId, sceneSpace);
  useEffect(() => {
    loadDefaultCamera.fitCameraToSceneDefault();
  }, [loadDefaultCamera])
  return <></>
}

const RevealComponent = ({
  clientConfig,
  sceneExternalId,
  sceneSpace,
  selectedAssetIdsArg,
  clippingPlanes,
  defaultNodeAppearance,
  styled_node_collections,
  height
}: {
  clientConfig: StClientConfig
  sceneExternalId: string
  sceneSpace: string
  selectedAssetIdsArg: number[]
  clippingPlanes: THREE.Plane[]
  defaultNodeAppearance?: NodeAppearance
  styled_node_collections: any[]
  height: number
}) => {
  useEffect(() => {
    Streamlit.setFrameHeight(height)
  }, [height])

  const sdk = useMemo(() => {
    const sdk = new CogniteClient({
      project: clientConfig.project,
      baseUrl: clientConfig.baseUrl,
      appId: "streamlit-reveal-component",
      getToken: async () => {
        return clientConfig.token
      },
    })
    return sdk;
  }, [clientConfig]);

  return sdk === null ? (
    <>Loading ...</>
  ) : (
    <RevealContext viewerOptions={{useFlexibleCameraManager: true}} sdk={sdk}>
      <div style={{height: height}}>
        <RevealCanvas>
          <RevealToolbar />
          <AxisGizmo />
          
          <LoadDefaultCamera sceneExternalId={sceneExternalId} sceneSpace={sceneSpace} />
          <ClippingPlanes planes={clippingPlanes} />
          <ApplyStyledNodeCollections sdk={sdk} styledNodeCollections={styled_node_collections} />
          <StateComponent sceneExternalId={sceneExternalId} sceneSpace={sceneSpace} selectedAssetIdsArg={selectedAssetIdsArg} defaultAppearance={defaultNodeAppearance} />
        </RevealCanvas>
      </div>
    </RevealContext>
  )
}

class StreamlitComponent extends StreamlitComponentBase<StState> {

  public render = (): ReactNode => {
    const config: StClientConfig = this.props.args["client_config"]
    const selectedAssetIds: number[] = this.props.args["selected_asset_ids"] ?? []
    const sceneExternalId: string = this.props.args["scene_external_id"]
    const space: string = this.props.args["scene_space"]
    const clippingPlanes: number[][] = this.props.args["clipping_planes"] ?? []
    const defaultNodeAppearance: NodeAppearance = getNodeAppearanceFromString(this.props.args["default_node_appearance"] ?? "Default")
    const styled_node_collections: any[] = this.props.args["styled_node_collections"] ?? []
    const height = this.props.args["height"] ?? 500
    
    return (
      <RevealComponent 
        sceneExternalId={sceneExternalId}
        clippingPlanes={getClippingPlanesFromArgs(clippingPlanes)}
        sceneSpace={space}
        clientConfig={config}
        selectedAssetIdsArg={selectedAssetIds}
        defaultNodeAppearance={defaultNodeAppearance}
        styled_node_collections={styled_node_collections}
        height={height}
      />
    )
  }
}

export default withStreamlitConnection(StreamlitComponent)
