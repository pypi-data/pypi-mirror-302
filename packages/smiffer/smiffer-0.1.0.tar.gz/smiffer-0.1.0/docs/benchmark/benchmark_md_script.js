/**
 * @fileoverview Functions for manipulating and checking structures in a web
 *               application. 
 * @author Lucas ROUAUD
 * @version 0.0.1
 * @date 15-07-2024
 * @license MIT
 *
 * This script provides functionalities to dynamically update web page elements
 * and URLs based on user select data. It is intended to enhance the user
 * interaction to see PDB structure from the benchmark.
 */

// Contain all PDB from the benchmark.
let PDB_ID = [
    "1AKX",
    "1BG0",
    "1EBY",
    "1EHE",
    "1H7L",
    "1I9V",
    "1IQJ",
    "1OFZ",
    "2ESJ",
    "3DD0",
    "3EE4",
    "4F8U",
    "5BJO",
    "5M9W",
    "6E9A",
    "5KX9",
    "6TF3",
    "7OAX0",
    "7OAX1",
    "8EYV",
];

// Contain all PDB that are RNA.
let IS_NUCLEIC = [
    "1AKX",
    "1I9V",
    "2ESJ",
    "4F8U",
    "5BJO",
    "5KX9",
    "6TF3",
    "7OAX0",
    "7OAX1",
    "8EYV",
];

// Contain all field names to access.
let FIELD = [
    "apbs",
    "h_b_acceptor",
    "h_b_donor",
    "hydrophobic",
    "hydrophilic",
    "pi_stacking",
];

// Contain all field names, but more human readable.
let NAME = [
    "APBS",
    "Hydrogen bond acceptor",
    "Hydrogen bond donor",
    "Hydrophobicity*",
    "Hydrophilicity*",
    "Pi stacking",
];

/**
 * Populates a given HTML select element with options.
 *
 * @param {HTMLSelectElement} selector - The select element to populate.
 * @param {Array} option_array - Array of values for the options.
 * @param {Array} [name_array=null] - Array of display names for the options.
 *                                    If null, option_array values are used as
 *                                    display names.
 */
function set_selector(selector, option_array, name_array = null) {
    // Set the names to option values, if no array name is given.
    if (name_array == null) {
        name_array = option_array;
    }

    option_array.forEach((value, index) => {
        let option = document.createElement("option");

        option.text = name_array[index];
        option.value = value;

        selector.appendChild(option);
    });
}

/**
 * TODO: Obsolete, remove this function.
 * Checks if the given PDB ID is in the RNA list and disables the hydrophobic
 * option in the select element if it is.
 * 
 * @param {Array} rna_list - Array of PDB IDs representing RNA structures.
 */
function check_rna(rna_list) {
    let pdb_id_val = document.getElementById("pdb_id").value;

    // Select the hydrophobic option for the field selector.
    let hydrophobic = document.querySelectorAll(
        "select#field option[value=hydrophobic]"
    )[0];

    hydrophobic.disabled = false;

    if (rna_list.includes(pdb_id_val)) {
        hydrophobic.disabled = true;
    }
}

/**
 * Updates the URL with the given PDB ID and field value, setting the field
 * value to "h_b_acceptor" if the PDB ID is in the RNA list and the selected
 * field is "hydrophobic".
 *
 * @param {Array} rna_list - Array of PDB IDs representing RNA structures.
 */
function update(rna_list) {
    let pdb_id_val = document.getElementById("pdb_id").value;
    let field_val = document.getElementById("field").value;

    if (url.includes("?")) {
        url = url.split("?")[0];
    }

    // Hydrophobic cannot be selected for RNA structures.
    if (rna_list.includes(pdb_id_val) && field_val == "hydrophobic") {
        field_val = "h_b_acceptor";
    }

    location.href = `${url}?pdb_id=${pdb_id_val}&field=${field_val}`;
}

// Set up selectors.
set_selector(document.getElementById("pdb_id"), PDB_ID);
set_selector(document.getElementById("field"), FIELD, NAME);

// Get the current URL.
let url = window.location.href;

// Set the URL for the iframe. If no data are selected, refresh the page with
// default values.
if (url.includes("?")) {
    let process_url = url.split("?");
    process_url = process_url[process_url.length - 1];

    process_url.split("&").forEach((field) => {
        let [key, value] = field.split("=");

        // Selected option in function of data given through the URL.
        if (key == "pdb_id" || key == "field") {
            let option = `select#${key} option[value='${value}']`;
            document.querySelectorAll(option)[0].selected = true;
        }

        let pdb_id_val = document.getElementById("pdb_id").value;
        let field_val = document.getElementById("field").value;

        // Set the selection in mol* in function of selected option.
        let new_href = `../molstar.html?pdb_id=${pdb_id_val}&` + 
            `field=${field_val}`;
        document.getElementById("molstar").src = new_href;
    });
} else {
    location.href = `${url}?pdb_id=1AKX&field=h_b_acceptor`;
}
