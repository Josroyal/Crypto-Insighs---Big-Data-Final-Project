import { chromium } from "playwright";
import { MongoClient } from "mongodb";

const uri = "mongodb://localhost:27017";
const dbName = "extractedNewsBigDataDB";
const collectionName = "coinMarketCap";

const insightsArray = [];

const navigatorFn = async (index) => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto("https://coinmarketcap.com/");
  console.log("Página inicial cargada");

  await page.click(`tr:nth-of-type(${index})`);

  await page.waitForLoadState("load");
  console.log("Nueva página cargada");

  const insights = await page.$$eval(
    'div[data-role="content-wrapper"] p',
    (results) => results.map((el) => el.innerText)
  );

  insightsArray.push(...insights);

  await browser.close();
};

async function saveToMongoDB(data) {
  try {
    await client.connect();
    console.log("Conectado a MongoDB");
    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    const documents = data.map((text) => ({ insight: text }));

    const result = await collection.insertMany(documents);

    console.log(`${result.insertedCount} artículos guardados en MongoDB`);
  } catch (error) {
    console.error("Error al guardar en MongoDB:", error);
  } finally {
    await client.close();
    console.log("Conexión cerrada");
  }
}

await Promise.allSettled(
  [...Array(20).keys()].map(async (index) => await navigatorFn(index))
);

const client = new MongoClient(uri);

await saveToMongoDB(insightsArray);
