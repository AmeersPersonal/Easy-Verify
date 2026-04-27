import { Verifier } from "../features/wsVerification/Verification";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { useEffect, useRef, useState } from 'react';
import React from 'react'
import { useLocation } from "react-router-dom";
import Card from "@mui/material/Card";



// function getEmail() {
//   const location = useLocation();
//   const locationState = location.state;
//   console.log(locationState?.email);
//   if(!locationState?.email) {alert("No Email Detected, will error out!")}
//   return locationState?.email;
// }

function verifyText(isVerifying, verifyState, submitError) {
  let curText = ""
  console.log(verifyState)
  if (!isVerifying) {
    curText = "Click to Verify";
  } else if (submitError) {
    curText = "Error!"
  } else {
    switch (verifyState) {
      case "keyWait":
        curText = "Started Verification"
        break;
      case "verificationWait":
        curText = "Waiting for Verification"
        break;
      case "done":
        curText = "✅\nVerification Sucessful!"
        break;
      case "fail":
        curText = "Verification Failed"
        break;
      case "error":
        curText = "Error!"
        break;
      default:
        curText = "Invalid State";

    }
  }
  return (
    <Typography variant="h5">{curText}</Typography>
  );
}

function loadingCircle(isVerifying, verifyState) {
  let viewable = (verifyState == "keyWait" || verifyState == "verificationWait") && isVerifying;
  if (viewable) return (<img src="/loading.svg" width={200} height={200} />)
  return null;

}



function WebSocketVerifyPage() {
  const location = useLocation();
  const storedUser = JSON.parse(localStorage.getItem('user') || '{}');
  const email = location.state?.email || storedUser?.email || localStorage.getItem('accountEmail') || 'unknown';
  const userId = location.state?.userId ?? storedUser?.id ?? null;
  const isUserIdConfigured = userId !== null && typeof userId !== 'undefined';

  if(email === 'unknown' || userId === null) {
    alert("user is undefined, error!");
  }

  const [submitError, setSubmitError] = useState('');
  const [isVerifying, setIsVerifying] = useState();
  const [verifyState, setVerifyState] = useState("");

  const verifier = useRef(null);

  function handleSubmit(event) {
    event.preventDefault();
    setIsVerifying(true); setSubmitError('');

    if (!isUserIdConfigured) {
      setSubmitError('Please log in before verifying');
      return;
    }

    try {
      verifier.current.startConnect(String(userId));

      window.location.href = "easy-verify://verifyDemoClient";

    } catch (error) {
      console.log(error);
    }

  }
  useEffect(() => {
    verifier.current = new Verifier("ws://localhost:8765", {
      email: email,
      callback_url: "http://localhost:3000/api/auth/verify",
      userID: userId
    });
    const subscribe = verifier.current?.subscribe(setVerifyState);
    return subscribe;
  }, []);

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
      }}
    >
      <img src="/icon.png" width={200} height={200} />
      <Typography variant="h4">Access Content Below</Typography>
      <Card sx={{
        margin: '25px auto',
        padding: '15px',
        bgcolor: '#121212',
        color: '#f5f5f5',
      }}>
        <Typography variant="h5">This verification will use the email address: {email}</Typography>
      </Card>

      {loadingCircle}

      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 3,
          textAlign: "center",
        }}
      >
        <Button type="submit" variant="contained" size="large">
          Verify
        </Button>
        {verifyText(isVerifying, verifyState, submitError)}
      </Box>
    </Box>
  );
}

export default WebSocketVerifyPage;
