const database = require("../database/database");

exports.deleteMyMedi = async (request, response) => {
  const mediID = request.params.medicine_id;

  if (!mediID) {
    return response.status(400).json({ msg: "Medicine creation date is required" });
  }

  try {
    const result = await database.pool.query(
      "DELETE FROM mymedicine WHERE id = $1",
      [mediID]
    );

    if (result.rowCount === 0) {
      return response.status(404).json({ msg: "Medicine not found" });
    }

    return response.status(200).json({ msg: "Delete My Medicine List Success" });
  } catch (error) {
    return response.status(500).json({ msg: "Delete My Medicine List Fail", error: error.message });
  }
};

