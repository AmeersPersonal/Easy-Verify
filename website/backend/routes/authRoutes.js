const express = require("express");
const authController = require("../controllers/authController");

const router = express.Router();

router.post("/login", authController.login);
router.post("/register", authController.register);
router.post("/verify", authController.setVerification);
router.get("/verify-status", authController.verificationStatus);
router.get("/validate-email", authController.validateEmail);

module.exports = router;
