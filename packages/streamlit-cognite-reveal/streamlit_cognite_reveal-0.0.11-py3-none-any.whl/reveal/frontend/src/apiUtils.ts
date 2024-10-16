import { NodeAppearance, DefaultNodeAppearance } from "@cognite/reveal"
import * as THREE from "three"

export function getNodeAppearanceFromString(value: string): NodeAppearance {
  switch (value) {
    case "Default":
      return DefaultNodeAppearance.Default
    case "Outlined":
      return DefaultNodeAppearance.Outlined
    case "Hidden":
      return DefaultNodeAppearance.Hidden
    case "InFront":
      return DefaultNodeAppearance.InFront
    case "Ghosted":
      return DefaultNodeAppearance.Ghosted
    default:
      throw new Error(`Unknown DefaultNodeAppearance value: ${value}`)
  }
}

export function toCamelCase(snakeCaseString: string): string {
  return snakeCaseString
    .toLowerCase()
    .split("_")
    .map((word, index) => {
      if (index === 0) {
        return word
      }
      return word.charAt(0).toUpperCase() + word.slice(1)
    })
    .join("")
}

export function getClippingPlanesFromArgs(
  clippingPlanes: number[][]
): THREE.Plane[] {
  return clippingPlanes.map((planeData: number[]) => {
    const orientation = new THREE.Vector3(
      planeData[0],
      planeData[1],
      planeData[2]
    )
    const point = orientation.clone().multiplyScalar(planeData[3])
    const plane = new THREE.Plane().setFromNormalAndCoplanarPoint(
      orientation,
      point
    )
    return plane
  })
}
