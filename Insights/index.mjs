import { chromium } from "playwright";
import { extract } from "@extractus/article-extractor";
import { MongoClient } from "mongodb";

const uri = "mongodb://localhost:27017";
const dbName = "extractedNewsBigDataDB";
const collectionName = "articles";

const browser = await chromium.launch({ headless: true });

const page = await browser.newPage();

await page.goto(
  "https://www.google.com/search?q=crypto+news&sca_esv=872fab285cdd172a&rlz=1C1CHBD_esPE938PE938&biw=1920&bih=919&tbm=nws&sxsrf=ADLYWIKU1-0fZg_7XDJ7xVbt51UGB0WNnQ%3A1733010397858&ei=3aNLZ_aLNO6xwt0PuYC32A0&ved=0ahUKEwi27p_pnoWKAxXumLAFHTnADdsQ4dUDCA0&uact=5&oq=crypto+news&gs_lp=Egxnd3Mtd2l6LW5ld3MiC2NyeXB0byBuZXdzMgoQABiABBhDGIoFMgsQABiABBiRAhiKBTILEAAYgAQYkQIYigUyCxAAGIAEGJECGIoFMgsQABiABBiRAhiKBTIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAESIsHUMYEWMYEcAB4AJABAJgBhQOgAbcFqgEDMy0yuAEDyAEA-AEBmAICoAK-BcICBBAAGB7CAgsQABiABBiGAxiKBZgDAIgGAZIHAzMtMqAHiQk&sclient=gws-wiz-news"
);

const articles = await page.$$eval("div[data-hveid][data-ved]", (results) =>
  results
    .map((el) => el.querySelector("a")?.href)
    .filter((v, i, s) => v && s.indexOf(v) === i)
    .slice(1, 6)
);

const extractedArticles = await Promise.all(
  articles.map(async (article) => await extract(article))
);

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

await saveToMongoDB(extractedArticles);

await browser.close();
