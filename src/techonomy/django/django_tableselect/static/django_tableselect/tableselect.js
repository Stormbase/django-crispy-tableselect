// TODO: make this code compatible with dinosaurs (old browsers)
addEventListener("DOMContentLoaded", () => {
  const tableSelector = "[data-tableselect]";
  const selectAllCheckboxSelector = "input[type=checkbox][data-tableselect-select-all]";
  const ariaNarratorSelector = "[data-tableselect-narrator]";
  const rowCheckboxSelector = "input[type=checkbox][name]";

  const allSelectedTextAttribute = "data-trans-all-selected";
  const selectAllSelectedTextAttribute = "data-trans-select-all";
  const deselectAllSelectedTextAttribute = "data-trans-deselect-all";
  const numSelectedTextAttribute = "data-trans-num-selected";

  const allChecked = (nodes) => Array.from(nodes).every((node) => node.checked);
  const partiallyChecked = (nodes) =>
    Array.from(nodes).some((node) => node.checked);

  const tables = document.querySelectorAll(tableSelector);

  tables.forEach((table) => {
    const selectAllCheckbox = table.querySelector(selectAllCheckboxSelector);
    const rowCheckboxes = table.querySelectorAll(rowCheckboxSelector);
    const ariaNarrator = table.querySelector(ariaNarratorSelector);

    // Get text placeholders from data attributes
    const selectAllSelectedPlaceholder = selectAllCheckbox && selectAllCheckbox.getAttribute(
      selectAllSelectedTextAttribute
    );
    const deselectAllSelectedPlaceholder = selectAllCheckbox && selectAllCheckbox.getAttribute(
      deselectAllSelectedTextAttribute
    );
    const allSelectedPlaceholder = ariaNarrator.getAttribute(
      allSelectedTextAttribute
    );
    const numSelectedPlaceholder = ariaNarrator.getAttribute(
      numSelectedTextAttribute
    );

    // Responsible for updating the checked state and accessible label of the checkbox
    const updateSelectAllCheckboxState = () => {
      if (!selectAllCheckbox) {
        return;
      }

      let checked = partiallyChecked(rowCheckboxes);

      selectAllCheckbox.indeterminate =
        !allChecked(rowCheckboxes) && partiallyChecked(rowCheckboxes);
        selectAllCheckbox.checked = checked;

      const totalRows = rowCheckboxes.length;

      if (checked) {
        selectAllCheckbox.ariaLabel = deselectAllSelectedPlaceholder.replace(
          "%num%",
          totalRows
        );
      } else {
        selectAllCheckbox.ariaLabel = selectAllSelectedPlaceholder.replace(
          "%num%",
          totalRows
        );
      }
    };

    // Responsible for generating an announcement for screenreader users with the intend
    // of giving them more context as to the current state of the table.
    // Example announcement: 10 of 25 selected
    const updateNarrator = () => {
      const totalRows = rowCheckboxes.length;
      const currentRowsSelected = Array.from(rowCheckboxes).filter(
        (box) => box.checked
      ).length;

      let text = "";

      // All rows are selected
      if (currentRowsSelected === totalRows) {
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
    const initializeSelectAllCheckbox = () => {
      if (!selectAllCheckbox) {
        return;
      }
      selectAllCheckbox.addEventListener("change", (event) => {
        const checked = event.target.checked;
        rowCheckboxes.forEach((box) => (box.checked = checked));
        updateSelectAllCheckboxState();
      });
    };

    // Responsible for setting up an event handler on each row checkbox
    const initializeSelectCheckboxes = () => {
      rowCheckboxes.forEach((box) => {
        box.addEventListener("change", () => {
          updateSelectAllCheckboxState();
          updateNarrator();
        });
      });
    };

    // Bring it all to live
    updateSelectAllCheckboxState();
    initializeSelectAllCheckbox();
    initializeSelectCheckboxes();
  });
});
