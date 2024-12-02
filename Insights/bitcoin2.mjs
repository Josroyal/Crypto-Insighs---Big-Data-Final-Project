import { chromium } from "playwright";
import { extract } from "@extractus/article-extractor";
import { MongoClient } from "mongodb";

const uri = "mongodb://localhost:27017";
const dbName = "extractedNewsBigDataDB";
const collectionName = "bitcoin";

const browser = await chromium.launch({ headless: true });

const page = await browser.newPage();

await page.goto(
  "https://www.google.com/search?sca_esv=e0e85ad122f2e6e2&rlz=1C1CHBD_esPE938PE938&sxsrf=ADLYWILYCoD6lnLCKaFZMAP7xDgY_nPLXg:1733021043469&q=bitcoin&tbm=nws&source=lnms&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWtG_mNb-HwafvV8cKK_h1a0WYAF4mXQP8CuyQXqW6TNzkZZ7jOZKM_gGu23cm0qZLxFh4eeiF1xrrVlLMaTv1YQSLQcqZdVh8AIxCCT3SFvQ11kmOrVyjXWszK6QaS4-v6lZ7jR8WBwuasm1qzJ1UmERHhRLslxZ6EZLAHQn9nO4s8dBnOEHGlwpMHtgJi0u0o_Ccfw&sa=X&ved=2ahUKEwi4qLy9xoWKAxU0fDABHea0JzUQ0pQJegQIFxAB&biw=2560&bih=1279&dpr=1"
);

const articles = await page.$$eval("div[data-hveid][data-ved]", (results) =>
  results
    .map((el) => el.querySelector("a")?.href)
    .filter((v, i, s) => v && s.indexOf(v) === i)
    .slice(1, 10)
);

const extractedArticles = await Promise.allSettled(
  articles.map(async (article) => await extract(article))
);

const filteredArticles = extractedArticles
  .filter((article) => article.status === "fulfilled")
  .map((article) => article.value)
  .slice(0, 5);

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

await saveToMongoDB(filteredArticles);

await browser.close();
