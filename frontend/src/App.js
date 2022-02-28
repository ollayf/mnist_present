import React, {useLayoutEffect, useState} from "react";
const offset = -80
// const generator = rough.generateFromMetadata()

const App = () => {
    const [drawing, setDrawing] = useState(false)

    useLayoutEffect( () => {
        const canvas = document.getElementById("canvas");

        const context = canvas.getContext('2d');
        context.lineWidth = 40;
        context.lineCap = "round";
    });

    function retrieveContext() {
        const canvas = document.getElementById("canvas");
        const context = canvas.getContext("2d");
        return context;
    }

    function retrieveCanvas() {
        return document.getElementById("canvas");
    }

    function initiatePath(x, y, context) {
        context.beginPath();
        context.moveTo(x, y);
    }

    function step(x, y, context) {
        y += offset;
        context.lineTo(x, y);
        context.stroke();
        initiatePath(x, y, context);
    }

    function clearCanvas(canvas, context) {
        context.clearRect(0, 0, canvas.width, canvas.height);
    }

    function submit() {
        const canvas = retrieveCanvas();
        const context = retrieveContext();
        clearCanvas(canvas, context);
    }

    function clearButton () {
        const canvas = retrieveCanvas();
        const context = retrieveContext();
        clearCanvas(canvas, context);
    }
    
    const handleMouseDown = (event) => {
        setDrawing(true);
        const context = retrieveContext();
        var {clientX, clientY} = event;
        clientY += offset;
        initiatePath(clientX, clientY, context);
    }

    const handleMouseMove = (event) => {
        if (!drawing) return;
        const {clientX, clientY} = event;
        const context = retrieveContext();
        step(clientX, clientY, context);
    }

    const handleMouseUp = () => {
        setDrawing(false);
        const context = retrieveContext();
        context.stroke();
    }

    return (
        <div>
            <canvas id="canvas" 
                
                width={0.7 * window.innerHeight} 
                height={0.7 * window.innerHeight}
                style={{
                    border: '2px solid #000',
                  }}
                onMouseDown= {handleMouseDown}
                onMouseMove= {handleMouseMove}
                onMouseUp= {handleMouseUp}
            >
                Canvas
            </canvas>
            <button onClick={submit}>
                Submit
            </button>
            <button onClick={clearButton}>
                Clear
            </button>
        </div>
        );
}

export default App;
