const database = require("../database/database"); // database 모듈 import

exports.getMyMedi = async (request, response) => {
  const userId = request.params.user_id; // 요청 URL에서 userID 파라미터 추출
  // console.log(userId);
  try {
    const result = await database.pool.query(
      "SELECT m.id AS medicine_id, m.medi_name, m.company_name, m.buying_date, m.exp_date, m.main_symptom, m.memo, m.created_at, m.notification, u.email AS user_email FROM mymedicine m JOIN users u ON m.user_id = u.id WHERE u.id = $1;",
      [userId]
    );

    return response.status(200).json(result.rows);
  } catch (error) {
    // 오류가 발생하여 응답에 실패했을 때 500 상태 코드와 error 메시지를 응답 결과로 전송
    return response.status(500).json({ msg: "Get My Medicine DataFail: " + error });
  }
};