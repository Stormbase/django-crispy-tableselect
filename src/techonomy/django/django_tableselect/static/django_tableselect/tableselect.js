// TODO: make this code compatible with dinosaurs (old browsers)
addEventListener("DOMContentLoaded", () => {
  const tableSelector = "[data-tableselect]";
  const bulkCheckboxSelector = "input[type=checkbox][data-bulk-select]";
  const ariaNarratorSelector = "[data-tableselect-narrator]";
  const selectCheckboxSelector = "input[type=checkbox][name]";

  const allSelectedTextAttribute = "data-trans-all-selected";
  const selectAllSelectedTextAttribute = "data-trans-select-all";
  const deselectAllSelectedTextAttribute = "data-trans-deselect-all";
  const numSelectedTextAttribute = "data-trans-num-selected";

  const allChecked = (nodes) => Array.from(nodes).every((node) => node.checked);
  const partiallyChecked = (nodes) =>
    Array.from(nodes).some((node) => node.checked);

  const tables = document.querySelectorAll(tableSelector);

  tables.forEach((table) => {
    const bulkCheckbox = table.querySelector(bulkCheckboxSelector);
    const selectCheckBoxes = table.querySelectorAll(selectCheckboxSelector);
    const ariaNarrator = table.querySelector(ariaNarratorSelector);

    let initialized = false;

    // No bulk checkbox = bulk select not enabled.
    // No point in initializing further.
    if (!bulkCheckbox) return;

    // Get text placeholders from data attributes
    const selectAllSelectedPlaceholder = bulkCheckbox.getAttribute(
      selectAllSelectedTextAttribute
    );
    const deselectAllSelectedPlaceholder = bulkCheckbox.getAttribute(
      deselectAllSelectedTextAttribute
    );
    const allSelectedPlaceholder = bulkCheckbox.getAttribute(
      allSelectedTextAttribute
    );
    const numSelectedPlaceholder = bulkCheckbox.getAttribute(
      numSelectedTextAttribute
    );

    // Responsible for updating the checked state and accessible label of the checkbox
    const updateBulkCheckboxState = () => {
      let checked = partiallyChecked(selectCheckBoxes);

      bulkCheckbox.indeterminate =
        !allChecked(selectCheckBoxes) && partiallyChecked(selectCheckBoxes);
      bulkCheckbox.checked = checked;

      const totalRows = selectCheckBoxes.length;

      if (checked) {
        bulkCheckbox.ariaLabel = deselectAllSelectedPlaceholder.replace(
          "%num%",
          totalRows
        );
      } else {
        bulkCheckbox.ariaLabel = selectAllSelectedPlaceholder.replace(
          "%num%",
          totalRows
        );
      }

      // We only want to narrate screenreaders announcements when the page changes, not upon initialization
      if (initialized) {
        updateNarrator();
      }
    };

    // Responsible for generating an announcement for screenreader users with the intend
    // of giving them more context as to the current state of the table.
    // Example announcement: 10 of 25 selected
    const updateNarrator = () => {
      const totalRows = selectCheckBoxes.length;
      const currentRowsSelected = Array.from(selectCheckBoxes).filter(
        (box) => box.checked
      ).length;

      let text = "";

      // All rows are selected
      if (currentRowsSelected == totalRows) {
        text = allSelectedPlaceholder.replace("%total%", totalRows);
      }
      // X out of Y are selected
      else {
        text = numSelectedPlaceholder
          .replace("%current%", currentRowsSelected)
          .replace("%total%", totalRows);
      }

      // Screenreaders will automatically pick up the changed text due to aria-live="polite"
      ariaNarrator.textContent = text;
    };

    // Responsible for setting up an event handler to check/uncheck all row checkboxes
    const initializeBulkCheckbox = () => {
      bulkCheckbox.addEventListener("change", (event) => {
        const checked = event.target.checked;
        selectCheckBoxes.forEach((box) => (box.checked = checked));
        updateBulkCheckboxState();
      });
    };

    // Responsible for setting up an event handler on each row checkbox
    const initializeSelectCheckboxes = () => {
      selectCheckBoxes.forEach((box) => {
        box.addEventListener("change", () => {
          updateBulkCheckboxState();
        });
      });
    };

    // Bring it all to live
    updateBulkCheckboxState();
    initializeBulkCheckbox();
    initializeSelectCheckboxes();

    initialized = true;
  });
});
