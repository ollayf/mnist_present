import React, {useLayoutEffect, useState} from "react";
import Result from './components/ResultComponent';
const RESULTANT_SIZE = 28

function resizeImage(image, height, width) {
    const h_diff = Math.floor(height / RESULTANT_SIZE)
    const w_diff = Math.floor(width / RESULTANT_SIZE)
    var result = []
    for (var i = 0; i < RESULTANT_SIZE; i += 1) {
        result.push([])
        var row = result[i]
        var row_start = 4 * i * h_diff * width 
        for (var j = 0; j < RESULTANT_SIZE; j += 1) {
            const index = row_start + j * w_diff * 4 + 3
            if (image[index]) {
                row.push(1)
            } else {
                row.push(0)
            }
        }
    }

    return result;
}

// function countValues(image) {
//     var count = 0;
//     image.forEach((element) => {
//         if (image[element]) {
//         count += 1;
//         }
//     });
//     console.log(count);
// }

function getResult(result_tensor) {
    var largest_i = 0;
    var largest_val = 0;
    for (var i = 0; i < 10; i += 1) {
        if (result_tensor[i] > largest_val) {
            largest_val = result_tensor[i]
            largest_i = i
        }
    }
    return largest_i
}

function getRealCoords(event, canvas) {
    const rect = canvas.getBoundingClientRect();
    var {clientX, clientY} = event;
    clientX = clientX - rect.left;
    clientY = clientY - rect.top
    return { clientX, clientY }
}

const App = () => {

    const [canvas, setCanvas] = useState(null);
    const [context, setContext] = useState(null);
    const [drawing, setDrawing] = useState(false);
    const [result, setResult] = useState(-1);
    const [confidence, setConfidence] = useState(0);
    const [ultraInstinctMode, setUlIn] = useState(false);
    
    useLayoutEffect( () => {
        const canvas = document.getElementById("canvas");
        
        const context = canvas.getContext('2d');
        context.lineWidth = canvas.height/8;
        context.lineCap = "round";
        context.filter = 'grayscale(1)';
        
        setCanvas(canvas);
        setContext(context);

    });

    function inference(image) {
        // create a new XMLHttpRequest
        var xhr = new XMLHttpRequest()
    
        // get a callback when the server responds
        xhr.addEventListener('load', () => {
          // update the state of the component with the result here
          var result = JSON.parse(xhr.responseText)
          result = result.predictions[0]
          console.log(result)
          const value = getResult(result)
          const confidence = result[value]
          console.log(result, confidence)
          setConfidence(confidence)
          setResult(value)
          console.log()
        })
        // open the request with the verb and the url
        xhr.open('POST', 'http://13.215.15.247:8501/v1/models/digit_recognition:predict')
        // send the request
        xhr.send(JSON.stringify({ "instances": image}))
    }

    function initiatePath(x, y, context) {
        context.beginPath();
        context.moveTo(x, y);
    }

    function step(x, y, context) {
        context.lineTo(x, y);
        context.stroke();
        initiatePath(x, y, context);
    }

    function clearCanvas() {
        context.clearRect(0, 0, canvas.width, canvas.height);
    }


    function submit() {
        console.log(0.7*window.innerHeight);
        var image = context.getImageData(0, 0, canvas.width, canvas.height).data;
        console.log(image);
        var result = resizeImage(image, canvas.height, canvas.width);
        inference(result);
        clearCanvas(canvas, context);
    }
    
    const handleMouseDown = (event) => {
        setDrawing(true);
        var {clientX, clientY} = getRealCoords(event, canvas)
        initiatePath(clientX, clientY, context);
    }

    const handleMouseMove = (event) => {
        if (!drawing) return;
        const {clientX, clientY} = getRealCoords(event, canvas);
        step(clientX, clientY, context);
    }

    const handleMouseUp = () => {
        setDrawing(false);
        context.stroke();
    }

    const ultraInstinct = () => {
        setUlIn(true);
    }

    return (
        <div>
            <div>
                <canvas id="canvas" 
                    
                    width={Math.floor(0.7 * window.innerHeight)} 
                    height={Math.floor(0.7 * window.innerHeight)}
                    style={{
                        border: '2px solid #000',
                    }}
                    onMouseDown= {handleMouseDown}
                    onMouseMove= {handleMouseMove}
                    onMouseUp= {handleMouseUp}
                >
                    Canvas
                </canvas>
            </div>
            <lb></lb>
            <button onClick={submit}>
                Submit
            </button>
            <button onClick={clearCanvas}>
                Clear
            </button>
            <button onClick={ultraInstinct}>
                Ultra Instinct
            </button>
            <Result confidence={confidence} result={result}></Result>
        </div>
        );
}

export default App;
