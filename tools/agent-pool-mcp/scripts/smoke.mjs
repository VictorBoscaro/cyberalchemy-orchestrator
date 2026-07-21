// Deterministic smoke test — runs the no-LLM paths so it needs no API key.
import { checkVocab, searchPool, prefilter } from "../src/select.mjs";
import { loadPool, POOL_PATH } from "../src/pool.mjs";

const p = loadPool();
console.log(`pool: ${POOL_PATH}`);
console.log(`entries=${p.entries.length} tagged=${p.tagged.length} vocab=${p.vocab.size}\n`);

console.log("check_vocab([category-theory, sheaf-semantics, not-a-real-tag]):");
console.log(JSON.stringify(checkVocab(["category-theory", "sheaf-semantics", "not-a-real-tag"]), null, 2), "\n");

console.log("search_pool({tags:[category-theory,fixed-point-theory], role:explorer, k:6}):");
console.log(JSON.stringify(searchPool({ tags: ["category-theory", "fixed-point-theory"], role: "explorer", k: 6 }), null, 2), "\n");

const pf = prefilter({ tags: ["category-theory"], role: "explorer" });
console.log(`prefilter(category-theory): candidates=${pf.candidates.length} neighborhood=${pf.neighborhood.length}`);
