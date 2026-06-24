import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = path.resolve(".");
const projectArg = process.argv[2] ?? "rain_gate_demo";
const project = path.isAbsolute(projectArg) ? projectArg : path.join(root, "02_projects", projectArg);
const projectName = path.basename(project);
const scriptFilter = process.argv[3] ?? "";
const scriptDir = path.join(project, "02_generated_content", "scripts", "csv");
const outputBaseName = scriptFilter ? path.basename(scriptFilter, ".csv") : "VN_Workbench_Template";
const outPath = path.join(project, "02_generated_content", "scripts", "excel", `${outputBaseName}.xlsx`);
const previewDir = path.join(project, "04_quality", "previews");

const headers = [
  "scene_id",
  "beat_id",
  "row_type",
  "speaker",
  "text",
  "voice_target",
  "expression",
  "body_action",
  "bg",
  "bgm",
  "sfx",
  "choice_group",
  "choice_text",
  "choice_target",
  "condition",
  "effects",
  "memory_refs",
  "qa_notes",
];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let inQuotes = false;
  const source = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  for (let i = 0; i < source.length; i += 1) {
    const ch = source[i];
    if (inQuotes) {
      if (ch === '"' && source[i + 1] === '"') {
        cell += '"';
        i += 1;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        cell += ch;
      }
      continue;
    }
    if (ch === '"') {
      inQuotes = true;
    } else if (ch === ",") {
      row.push(cell);
      cell = "";
    } else if (ch === "\n") {
      row.push(cell);
      if (row.some((value) => value !== "")) {
        rows.push(row);
      }
      row = [];
      cell = "";
    } else {
      cell += ch;
    }
  }
  row.push(cell);
  if (row.some((value) => value !== "")) {
    rows.push(row);
  }
  return rows;
}

function flattenObject(prefix, value, out = []) {
  if (Array.isArray(value)) {
    out.push([prefix, value.map((v) => (typeof v === "string" ? v : JSON.stringify(v))).join(" | ")]);
  } else if (value && typeof value === "object") {
    for (const [k, v] of Object.entries(value)) {
      flattenObject(prefix ? `${prefix}.${k}` : k, v, out);
    }
  } else {
    out.push([prefix, value ?? ""]);
  }
  return out;
}

async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function listJsonFiles(dirPath) {
  if (!(await pathExists(dirPath))) {
    return [];
  }
  return (await fs.readdir(dirPath)).filter((name) => name.endsWith(".json")).sort();
}

async function readJsonFile(filePath, fallback = {}) {
  if (!(await pathExists(filePath))) {
    return fallback;
  }
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

async function readJsonRel(rel, fallback = {}) {
  return readJsonFile(path.join(project, rel), fallback);
}

const characterDir = path.join(project, "00_project_memory", "cards", "characters");
const characterFiles = await listJsonFiles(characterDir);
const characters = [];
for (const file of characterFiles) {
  characters.push(await readJsonFile(path.join(characterDir, file)));
}

const sceneDir = path.join(project, "01_narrative_design", "scenes", "scene_cards");
const sceneFiles = await listJsonFiles(sceneDir);
const sceneFile = sceneFiles[0] ?? null;
const scene = sceneFile
  ? await readJsonFile(path.join(sceneDir, sceneFile))
  : { scene_id: "", title: "", route: "", location: "", time: "", usable_objects: [] };
const sceneId = scene.scene_id ?? sceneFile?.replace("_scene_card.json", "") ?? "S001";

const deltaDir = path.join(project, "01_narrative_design", "scenes", "state_deltas");
const deltaFiles = await listJsonFiles(deltaDir);
const matchingDelta = deltaFiles.find((name) => name === `${sceneId}_state_delta.json`) ?? deltaFiles[0] ?? null;
const delta = matchingDelta ? await readJsonFile(path.join(deltaDir, matchingDelta)) : {};
const route = await readJsonRel("01_narrative_design/routes/route_map.json", { variables: [] });
const routeVariables = Array.isArray(route.variables) ? route.variables : [];
const usableObjects = Array.isArray(scene.usable_objects) ? scene.usable_objects : [];

let scriptFiles = (await fs.readdir(scriptDir)).filter((name) => name.endsWith(".csv")).sort();
if (scriptFilter) {
  scriptFiles = scriptFiles.filter((name) => name === scriptFilter || name === `${scriptFilter}.csv`);
  if (scriptFiles.length === 0) {
    throw new Error(`No CSV matched script filter: ${scriptFilter}`);
  }
}
const scriptRowsByFile = [];
for (const file of scriptFiles) {
  const rows = parseCsv(await fs.readFile(path.join(scriptDir, file), "utf8"));
  scriptRowsByFile.push({ file, rows });
}
const scriptRows = [
  scriptRowsByFile[0]?.rows[0] ?? headers,
  ...scriptRowsByFile.flatMap(({ rows }) => rows.slice(1)),
];
const lastScriptRow = scriptRows.length;
const scriptDataRows = scriptRows.slice(1);
const countRows = (predicate) => scriptDataRows.filter(predicate).length;
const blankRowTypeCount = countRows((r) => !r[2]);
const missingVoiceCount = countRows((r) => r[2] === "dialogue" && !r[5]);
const bodyActionCount = countRows((r) => Boolean(r[7]));
const missingChoiceTargetCount = countRows((r) => r[2] === "choice" && !r[13]);
const effectsCount = countRows((r) => Boolean(r[15]));
const memoryRefsCount = countRows((r) => Boolean(r[16]));
const dialogueCount = countRows((r) => r[2] === "dialogue");

const workbook = Workbook.create();

function styleHeader(sheet, range) {
  sheet.getRange(range).format = {
    fill: "#1F6F78",
    font: { bold: true, color: "#FFFFFF" },
    wrapText: true,
  };
}

function border(sheet, range) {
  sheet.getRange(range).format.borders = { preset: "all", style: "thin", color: "#D7DEE2" };
}

const start = workbook.worksheets.add("Start");
start.showGridLines = false;
start.getRange("A1:H1").merge();
start.getRange("A1").values = [["VN Fusion Workbench"]];
start.getRange("A1").format = {
  fill: "#153E46",
  font: { bold: true, color: "#FFFFFF", size: 18 },
};
start.getRange("A3:B9").values = [
  ["Purpose", "Write visual novel scripts with fixed character voice, state deltas, and exportable rows."],
  ["Script sheet", "One row per textbox beat, choice row, or command."],
  ["Required rhythm", "Use body_action and memory_refs frequently; avoid abstract emotion labels."],
  ["Validation", "Run 00_workbench_core/tools/vn_workbench.py validate before exporting."],
  ["WebGAL export", "Run 00_workbench_core/tools/vn_workbench.py export-webgal after CSV save."],
  ["Source CSV", `02_projects/${projectName}/02_generated_content/scripts/csv/${scriptFilter || "*.csv"}`],
  ["Borrowed projects", "See 01_reference_log/open_source_round_2026_06_18/notes/borrowed_projects.md and AI_HANDOFF_PACKAGE/source_ledgers/OPEN_SOURCE_BORROWING_LEDGER.md"],
];
start.getRange("A3:A9").format = { fill: "#DDEFF1", font: { bold: true } };
start.getRange("A3:B9").format.wrapText = true;
border(start, "A3:B9");
start.getRange("A:A").format.columnWidthPx = 190;
start.getRange("B:B").format.columnWidthPx = 620;

const script = workbook.worksheets.add("Script");
script.getRangeByIndexes(0, 0, scriptRows.length, scriptRows[0].length).values = scriptRows;
styleHeader(script, "A1:R1");
border(script, `A1:R${scriptRows.length}`);
script.freezePanes.freezeRows(1);
script.getRange("A:R").format.wrapText = true;
script.getRange("A:A").format.columnWidthPx = 90;
script.getRange("B:B").format.columnWidthPx = 100;
script.getRange("C:C").format.columnWidthPx = 90;
script.getRange("D:D").format.columnWidthPx = 110;
script.getRange("E:E").format.columnWidthPx = 360;
script.getRange("F:H").format.columnWidthPx = 190;
script.getRange("I:K").format.columnWidthPx = 120;
script.getRange("L:O").format.columnWidthPx = 130;
script.getRange("P:R").format.columnWidthPx = 190;
script.getRange("C2:C200").dataValidation = {
  rule: { type: "list", values: ["dialogue", "narration", "thought", "choice", "command", "comment"] },
};

const chars = workbook.worksheets.add("CharacterCards");
const charHeader = ["id", "name", "role", "desire", "fear", "default_rhythm", "pressure_rhythm", "vocabulary", "dodge", "example_pressured"];
const charRows = characters.map((c) => {
  const fp = c.speech_fingerprint ?? {};
  const examples = c.example_dialogue?.pressured ?? c.example_dialogue?.default ?? [];
  return [
    c.id ?? "",
    c.name ?? "",
    c.role ?? "",
    c.desire ?? "",
    c.fear ?? "",
    fp.default_rhythm ?? "",
    fp.pressure_rhythm ?? "",
    Array.isArray(fp.vocabulary) ? fp.vocabulary.join(" / ") : "",
    fp.dodge ?? "",
    Array.isArray(examples) ? examples.join(" | ") : "",
  ];
});
if (charRows.length === 0) {
  charRows.push([
    "MISSING",
    "No character cards",
    "Add JSON files under 00_project_memory/cards/characters",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
  ]);
}
chars.getRangeByIndexes(0, 0, charRows.length + 1, charHeader.length).values = [charHeader, ...charRows];
styleHeader(chars, "A1:J1");
border(chars, `A1:J${charRows.length + 1}`);
chars.freezePanes.freezeRows(1);
chars.getRange("A:J").format.wrapText = true;
chars.getRange("A:B").format.columnWidthPx = 120;
chars.getRange("C:E").format.columnWidthPx = 220;
chars.getRange("F:J").format.columnWidthPx = 260;

const sceneSheet = workbook.worksheets.add("SceneCard");
const sceneCore = [
  ["scene_id", scene.scene_id],
  ["title", scene.title],
  ["route", scene.route],
  ["location", scene.location],
  ["time", scene.time],
  ["entering_pressure", scene.entering_pressure],
  ["player_want", scene.player_want],
  ["choice_pressure", scene.choice_pressure],
  ["exit_image", scene.exit_image],
];
sceneSheet.getRangeByIndexes(0, 0, sceneCore.length, 2).values = sceneCore;
styleHeader(sceneSheet, "A1:B1");
sceneSheet.getRange("A1:B9").format.wrapText = true;
border(sceneSheet, "A1:B9");
sceneSheet.getRange("A:A").format.columnWidthPx = 180;
sceneSheet.getRange("B:B").format.columnWidthPx = 660;
sceneSheet.getRange("D1:G1").values = [["object_id", "type", "description", "dramatic_use"]];
const objectRows = usableObjects.length
  ? usableObjects.map((o) => [
      o.object_id ?? o.id ?? "",
      o.type ?? "",
      o.description ?? "",
      o.dramatic_use ?? "",
    ])
  : [["MISSING", "usable_object", "Add at least five operable objects to the scene card.", "The environment must change dialogue, evidence, cost, or memory."]];
sceneSheet.getRangeByIndexes(1, 3, objectRows.length, 4).values = objectRows;
styleHeader(sceneSheet, "D1:G1");
border(sceneSheet, `D1:G${objectRows.length + 1}`);
sceneSheet.getRange("D:G").format.wrapText = true;
sceneSheet.getRange("D:G").format.columnWidthPx = 190;

const deltaSheet = workbook.worksheets.add("StateDelta");
const deltaRows = flattenObject("", delta);
deltaSheet.getRangeByIndexes(0, 0, deltaRows.length + 1, 2).values = [["path", "value"], ...deltaRows];
styleHeader(deltaSheet, "A1:B1");
border(deltaSheet, `A1:B${deltaRows.length + 1}`);
deltaSheet.freezePanes.freezeRows(1);
deltaSheet.getRange("A:A").format.columnWidthPx = 260;
deltaSheet.getRange("B:B").format.columnWidthPx = 700;
deltaSheet.getRange("A:B").format.wrapText = true;

const qa = workbook.worksheets.add("QA Gates");
qa.getRange("A1:D1").values = [["Gate", "Rule", "Check value", "Status"]];
qa.getRange("A2:D9").values = [
  ["Form", "Script rows have required row_type", blankRowTypeCount, "0 blanks expected"],
  ["Voice", "Dialogue rows include voice_target", missingVoiceCount, "0 expected"],
  ["Body", "Body/action column used", bodyActionCount, "Review if low"],
  ["Choice", "Choice rows include targets", missingChoiceTargetCount, "0 expected"],
  ["State", "Effects column used", effectsCount, "Review if low"],
  ["Memory", "Memory refs used", memoryRefsCount, "Review if low"],
  ["Text", "Dialogue row count", dialogueCount, "Info"],
  ["Route", "Route variables count", routeVariables.length, "Info"],
];
styleHeader(qa, "A1:D1");
border(qa, "A1:D9");
qa.getRange("A:D").format.wrapText = true;
qa.getRange("A:A").format.columnWidthPx = 110;
qa.getRange("B:B").format.columnWidthPx = 260;
qa.getRange("C:C").format.columnWidthPx = 320;
qa.getRange("D:D").format.columnWidthPx = 160;

await fs.mkdir(previewDir, { recursive: true });
await fs.mkdir(path.dirname(outPath), { recursive: true });
for (const sheetName of ["Start", "Script", "CharacterCards", "SceneCard", "StateDelta", "QA Gates"]) {
  const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(path.join(previewDir, `${sheetName.replace(/\s+/g, "_")}.png`), new Uint8Array(await preview.arrayBuffer()));
}

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});
console.log(errors.ndjson);

const overview = await workbook.inspect({
  kind: "sheet,table",
  maxChars: 4000,
  tableMaxRows: 4,
  tableMaxCols: 8,
});
console.log(overview.ndjson);

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outPath);
console.log(`Wrote ${outPath}`);
