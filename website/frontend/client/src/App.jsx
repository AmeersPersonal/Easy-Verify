import { useState } from 'react'
import './App.css'

function App() {
  const [clickText, setClickText] = useState("");


  const test = () => {
    setClickText("Verifying...");
    
  }


  return (
    <>
      <div>
      
        <img src= "/icon.png" width={400} height={400}/>
        <h1>Access Content Below</h1> <br/>
        <form action={test}>
          <input/> <br/>
          <button type="submit">Verify</button>
        </form>


        <h3>{clickText}</h3>
      </div>
    </>
  )
}

export default App
