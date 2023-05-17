"use strict";
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

  /** Checks if nodes are checked. */
  const allChecked = (nodes) => Array.from(nodes).every((node) => node.checked);
  /** Checks if at least one node is checked. */
  const partiallyChecked = (nodes) =>
    Array.from(nodes).some((node) => node.checked);

  const tables = document.querySelectorAll(tableSelector);

  tables.forEach((table) => {
    const selectAllCheckbox = table.querySelector(selectAllCheckboxSelector);
    const rowCheckboxes = table.querySelectorAll(rowCheckboxSelector);
    const ariaNarrator = table.querySelector(ariaNarratorSelector);

    // Get text placeholders from data attributes
    const selectAllSelectedPlaceholder =
      selectAllCheckbox &&
      selectAllCheckbox.getAttribute(selectAllSelectedTextAttribute);
    const deselectAllSelectedPlaceholder =
      selectAllCheckbox &&
      selectAllCheckbox.getAttribute(deselectAllSelectedTextAttribute);
    const allSelectedPlaceholder = ariaNarrator.getAttribute(
      allSelectedTextAttribute
    );
    const numSelectedPlaceholder = ariaNarrator.getAttribute(
      numSelectedTextAttribute
    );

    let shiftPressed = false;
    let lastChangedCheckbox = null;

    document.addEventListener("keydown", (event) => {
      shiftPressed = event.shiftKey;
    });

    document.addEventListener("keyup", (event) => {
      shiftPressed = event.shiftKey;
    });

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

    /**
     * Updates the checked state of all checkboxes between the last changed checkbox and the given checkbox.
     * Used to implement the 'shift' select multiple pattern.
     */
    const updateAffectedCheckboxes = (currentCheckbox) => {
      if (!lastChangedCheckbox) {
        return;
      }

      const nodes = Array.from(rowCheckboxes);
      const targetIndex = nodes.findIndex((el) => el === currentCheckbox);
      const lastChangedIndex = nodes.findIndex(
        (el) => el === lastChangedCheckbox
      );

      const startIndex = Math.min(targetIndex, lastChangedIndex);
      const endIndex = Math.max(targetIndex, lastChangedIndex);
      const affectedCheckboxes = nodes.filter(
        (el, index) => startIndex <= index && index <= endIndex
      );

      // Update all affected checkboxes checked state.
      affectedCheckboxes.forEach(
        (el) => (el.checked = currentCheckbox.checked)
      );
      // Responsibility for updating the select all checkbox and narrator is delegated to
      // the `change` event handler of the currentCheckbox (see `initializeSelectCheckboxes` function).
    };

    // Responsible for setting up an event handler to check/uncheck all row checkboxes
    const initializeSelectAllCheckbox = () => {
      if (!selectAllCheckbox) {
        return;
      }
      selectAllCheckbox.addEventListener("change", (event) => {
        // Clear the last changed checkbox.
        lastChangedCheckbox = null;

        const checked = event.target.checked;
        rowCheckboxes.forEach((box) => (box.checked = checked));
        updateSelectAllCheckboxState();
      });
    };

    // Responsible for setting up an event handler on each row checkbox
    const initializeSelectCheckboxes = () => {
      rowCheckboxes.forEach((box) => {
        box.addEventListener("change", (event) => {
          // If shift was pressed during the change, all checkboxes between this checkbox
          // and ``lastChangedCheckbox`` are affected as well.
          if (shiftPressed) {
            updateAffectedCheckboxes(event.target);
          }
          lastChangedCheckbox = event.target;
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
