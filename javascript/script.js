document.addEventListener('DOMContentLoaded', function() {
    // Read text from file (assuming it's in the same directory as the HTML file)
    fetch('your_data.txt')
      .then(response => response.text())
      .then(data => displayData(data));
  });
  
  function displayData(data) {
    const container = document.getElementById('content');
    const lines = data.trim().split('\n');
  
    lines.forEach(line => {
      const [category, subcategories] = line.split(' - ');
  
      // Check if there are subcategories with values other than 0
      const hasNonZeroValues = subcategories.split(';').some(subcategory => {
        const [, value] = subcategory.split(',');
        return parseInt(value) !== 0;
      });
  
      if (hasNonZeroValues) {
        const categoryElement = document.createElement('div');
        categoryElement.className = 'category';
        categoryElement.textContent = category;
        container.appendChild(categoryElement);
  
        const subcategoryList = document.createElement('ul');
  
        subcategories.split(';').forEach(subcategory => {
          const [name, value] = subcategory.split(',');
  
          if (parseInt(value) !== 0) {
            const subcategoryElement = document.createElement('li');
            subcategoryElement.textContent = name;
  
            if (value > 0) {
              subcategoryElement.className = 'subcategory';
            } else if (value < 0) {
              subcategoryElement.className = 'subcategory negative';
            }
  
            subcategoryList.appendChild(subcategoryElement);
          }
        });
  
        categoryElement.appendChild(subcategoryList);
      }
    });
  }
  
