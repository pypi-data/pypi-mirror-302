import React, { useCallback, useEffect, useMemo, useRef, FC } from "react"

import {
  withStreamlitConnection,
  Streamlit,
  ComponentProps,
} from "streamlit-component-lib"

import { VTKViewer, VTKViewerDrawer, VTKFloatingToolbar } from "pollination-viewer"

import { Layout } from "antd"

import './VTKStreamlit.css'

import isequal from "lodash.isequal"
import debounce from "lodash.debounce"

const HEIGHT = 640

const VTKStreamlit: FC<ComponentProps> = ({
  args
}) => {
  const { 
    subscribe, 
    screenshot_name,
    action_stack,
    content,
    clear,
    style,
    toolbar,
    sider
  } = args

  const viewerRef = useRef<any>(null)

  // state returned to streamlit
  const [viewerState, setViewerState] = React.useState<any>({})
  const viewerSceneRef = useRef<any[]>([])

  // stack of actions to dispatch via vtkjs
  const actionStackRef = useRef<any[]>([])

  // file to be loaded
  const [file, setFile] = React.useState<Uint8Array | undefined>(undefined)

  const handleScreenshot = useCallback((fileName='VTKJSStreamlit') => {
    if (!viewerRef.current) return
    viewerRef.current.handleScreenshot(fileName, false)
  }, [])

  useEffect(() => {
    if (subscribe) {
      Streamlit.setComponentValue(viewerState)
    } else if (viewerState.scene && viewerState.scene.length > 0) {
      const scene = viewerState.scene.map(({id}: {id: string}) => id)
      const ref = viewerSceneRef.current.map(({id}: {id: string}) => id)

      if (isequal(scene, ref)) return
      
      viewerSceneRef.current = [...viewerState.scene]

      Streamlit.setComponentValue({
        scene: viewerSceneRef.current
      })
    }
  }, [viewerState, subscribe])

  // aggreate and dispatch actions on a debounced interval
  const dispatchActionStack = useCallback(() => {
    if (viewerRef.current && viewerRef.current.dispatch &&
      actionStackRef.current && actionStackRef.current.length > 0) {

      // handles screenshot as a special case
      const screenshotIndex = actionStackRef.current.findIndex(a => a.type === "streamlit-screenshot")
      if (screenshotIndex !== -1) {
        screenshot_name && handleScreenshot(screenshot_name)
      }

      // filters type === "strealit-screenshot", and actions with duplicate types
      // any action with ids [] will be dispatched
      const actions = [...actionStackRef.current].reverse()
        .filter((action, i, array) =>
          (action.type !== "streamlit-screenshot" &&
            typeof action.ids !== 'undefined') ||
          array.findIndex(a => a.type === action.type) === i
        )

      viewerRef.current.dispatch(actions)
      actionStackRef.current = []
    }
  }, [handleScreenshot, screenshot_name])

  const debouncedDispatch = useCallback(debounce(dispatchActionStack, 250, { leading:true, maxWait: 750 }), [dispatchActionStack])

  useEffect(() => {
    if (action_stack
      && viewerRef.current && viewerRef.current.dispatch) {
      actionStackRef.current = [
        ...actionStackRef.current,
        ...action_stack
      ]
      if (actionStackRef.current.length > 0) {
        debouncedDispatch()
      }
    }
  }, [action_stack, debouncedDispatch])

  useEffect(() => {
    if (content) {
      setFile(currFile => {
        if (!currFile) return content
        const equal = isequal(content, currFile)
        return equal ? currFile : content
      })
    }
  }, [content])
  
  const loadFile = (file: Uint8Array) => {
    if (viewerRef.current && viewerRef.current.dispatch && viewerRef.current.loadFile) {

      if(clear) viewerRef.current.dispatch({ type: 'remove-all' }, true)

      const scene = viewerSceneRef.current
      if (!scene) return

      const config = scene.length > 0 ? scene : undefined

      viewerRef.current.loadFile(new Blob([file]), 'vtkjs', config)
    }
  }

  useEffect(() => {
    if (!file) return
    loadFile(file)
  }, [file])

  useEffect(() => {
    if (style && 
        style.height && 
        style.height.includes('px')) {
          Streamlit.setFrameHeight(parseInt(style.height.replace('px', '')))
    } else {
      Streamlit.setFrameHeight(HEIGHT)
    }
  }, [style])

  const cssStyle = useMemo(() => {
    return style ?? { border: "1px solid #d0d7de", borderRadius: "2px", height: `${HEIGHT}px` }
  }, [style])

  return (
    <div style={{ 
      width: '100%', 
      height: `${HEIGHT}px`, 
      border: "1px solid #d0d7de", 
      borderRadius: "2px", 
      ...cssStyle, 
      display: 'flex' 
    }}>
      <Layout style={{ flexDirection: 'row' }}>
        {sider &&
          <VTKViewerDrawer 
            dispatch={viewerRef.current?.dispatch} 
            viewerState={viewerState} 
            handleScreenshot={handleScreenshot} />
        }
        <Layout>
          {toolbar &&
            <VTKFloatingToolbar 
              dispatch={viewerRef.current?.dispatch} 
              viewerState={viewerState} 
              handleScreenshot={handleScreenshot} />
          }
          <Layout.Content style={{ 
            display: 'flex', 
            flexDirection: 'column' 
          }}>
            <VTKViewer 
              setViewerState={setViewerState} 
              ref={viewerRef} />
          </Layout.Content>
        </Layout>
      </Layout>
    </div>
  )
}

export default withStreamlitConnection(VTKStreamlit)