"use strict";
const MongoClient = require("mongodb").MongoClient;

module.exports.readPost = async (event) => {
  const client = await MongoClient.connect(
    "mongodb+srv://garam:garam0201@cluster0.plpuyog.mongodb.net/?retryWrites=true&w=majority",
    {
      useUnifiedTopology: true,
    }
  );
  const db = client.db("emotion_diary");
  const collection = db.collection("post");

  const result = await collection.find().toArray();

  client.close();

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(result),
  };
};

module.exports.uploadPost = async (event) => {
  return {
    statusCode: 200,
    body: JSON.stringify(
      {
        message: "Go Serverless v1.0! Your function executed successfully!",
      },
      null,
      2
    ),
  };

  // Use this code if you don't use the http event with the LAMBDA-PROXY integration
  // return { message: 'Go Serverless v1.0! Your function executed successfully!', event };
};
