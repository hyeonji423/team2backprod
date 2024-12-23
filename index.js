const PORT = 8000;

const express = require("express");
const cors = require("cors");
const path = require("path");
const authRouter = require("./routes/authRoutes");
const myPageRouter = require("./routes/myPageRoutes");
const emailRouter = require("./routes/emailRoutes");
const searchRouter = require("./routes/searchRoutes");
const spawn = require("child_process").spawn;
const swaggerUi = require("swagger-ui-express");
const YAML = require("yamljs");
const swaggerDocument = YAML.load("./swagger.yaml");

const app = express();

app.use(cors());
app.use(express.json());



app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

app.get("/", (req, res) => {
  res.send("auth server test running");
});

app.use("/auth", authRouter); // http://localhost:8000/auth
app.use("/myPage", myPageRouter); // http://localhost:8000/myPage
app.use("/medicine", searchRouter);
app.use("/email", emailRouter);

// -- 이 사이에 챗봇 경로 추가해 주세요

app.post("/chat1", (request, response) => {
  try {
    const { question } = request.body;
    console.log(question);

    const scriptPath = path.join(__dirname, "chat1.py");
    const phythonPath = "python";

    const result = spawn(phythonPath, [scriptPath, question]);

    let answer = "";
    let hasResponded = false;

    // 파이썬 스크립트의 출력을 수신하는 이벤트 리스너
    result.stdout.on("data", (data) => {
      answer += data.toString();
    });

    // 파이썬 스크립트의 오류를 수신하는 이벤트 리스너
    result.stderr.on("data", (data) => {
      // USER_AGENT 관련 경고 메시지는 무시하고 다른 에러만 처리
      const errorMsg = data.toString();
      if (!errorMsg.includes("USER_AGENT") && !hasResponded) {
        hasResponded = true;
        console.error(errorMsg);
        response.status(500).json({
          answer: "error",
        });
      }
    });

    // 파이썬 스크립트의 종료를 수신하는 이벤트 리스너
    result.on("close", (code) => {
      if (!hasResponded) {
        hasResponded = true;
        if (code === 0) {
          response.status(200).json({
            answer,
          });
        } else {
          response.status(500).json({
            error: `Child process exited with code ${code}`,
          });
        }
      }
    });
  } catch (error) {
    if (!hasResponded) {
      response.status(500).json({ error: error.message });
    }
  }
});
// --

app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));
