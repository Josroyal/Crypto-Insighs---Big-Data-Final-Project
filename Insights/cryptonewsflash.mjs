import { chromium } from "playwright";
import { extract } from "@extractus/article-extractor";
import { MongoClient } from "mongodb";

const uri = "mongodb://localhost:27017";
const dbName = "extractedNewsBigDataDB";
const collectionName = "cryptoNewsFlash";

const browser = await chromium.launch({ headless: true });

const page = await browser.newPage();

await page.goto("https://www.crypto-news-flash.com/");

const articleURLS = await page.$$eval("article", (results) =>
  results.map((el) => el.querySelector("a")?.href)
);

const extractedArticles = await Promise.allSettled(
  articleURLS.map(async (article) => await extract(article))
);

const stripedArticles = extractedArticles
  .filter((article) => article.status === "fulfilled")
  .map((article) => ({
    ...article.value,
    content: article.value.content.replace(/<[^>]*>?/gm, ""),
  }));

const client = new MongoClient(uri);

async function saveToMongoDB(data) {
  try {
    await client.connect();
    console.log("Conectado a MongoDB");
    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    const result = await collection.insertMany(data);
    console.log(`${result.insertedCount} artículos guardados en MongoDB`);
  } catch (error) {
    console.error("Error al guardar en MongoDB:", error);
  } finally {
    await client.close();
    console.log("Conexión cerrada");
  }
}

saveToMongoDB(stripedArticles);

await browser.close();
