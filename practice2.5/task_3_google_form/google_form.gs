/**
 * Функція для створення Google Форми для збору даних
 * Створює форму з полями: ім'я, дата, відділ
 */
function createDataCollectionForm() {
  try {
    // Створюємо нову форму
    var form = FormApp.create('Форма збору даних співробітників');
    
    // Додаємо опис форми
    form.setDescription('Ця форма використовується для збору основної інформації про співробітників.');
    
    // Додаємо поле для введення імені (обов'язкове)
    var nameItem = form.addTextItem();
    nameItem.setTitle('Ім\'я та прізвище')
           .setRequired(true)
           .setHelpText('Введіть ваше повне ім\'я та прізвище');
    
    // Додаємо поле для вибору дати (обов'язкове)
    var dateItem = form.addDateItem();
    dateItem.setTitle('Дата')
           .setRequired(true)
           .setHelpText('Виберіть дату');
    
    // Додаємо поле для вибору відділу (обов'язкове)
    var departmentItem = form.addListItem();
    departmentItem.setTitle('Відділ')
                 .setRequired(true)
                 .setChoiceValues(['Маркетинг', 'Розробка', 'Продажі', 'HR', 'Фінанси', 'Інше'])
                 .setHelpText('Виберіть ваш відділ');
    
    // Додаємо поле для додаткових коментарів (необов'язкове)
    var commentItem = form.addParagraphTextItem();
    commentItem.setTitle('Додаткові коментарі')
              .setHelpText('За бажанням, додайте будь-які коментарі або додаткову інформацію');
    
    // Налаштовуємо підтвердження після відправки форми
    form.setConfirmationMessage('Дякуємо! Ваша відповідь була записана.');
    
    // Отримуємо URL форми
    var formUrl = form.getPublishedUrl();
    var editUrl = form.getEditUrl();
    
    // Виводимо URL форми в лог
    Logger.log('URL опублікованої форми: ' + formUrl);
    Logger.log('URL для редагування форми: ' + editUrl);
    
    return {
      success: true,
      formUrl: formUrl,
      editUrl: editUrl,
      message: 'Форму успішно створено!'
    };
  } catch (error) {
    Logger.log('Помилка при створенні форми: ' + error.toString());
    return {
      success: false,
      message: 'Помилка при створенні форми: ' + error.toString()
    };
  }
}

/**
 * Функція для отримання URL створеної форми
 * Використовується для отримання URL після створення форми
 */
function getFormUrl() {
  // Отримуємо всі форми, створені поточним користувачем
  var forms = FormApp.getActiveForm();
  
  if (forms) {
    var formUrl = forms.getPublishedUrl();
    var editUrl = forms.getEditUrl();
    
    Logger.log('URL опублікованої форми: ' + formUrl);
    Logger.log('URL для редагування форми: ' + editUrl);
    
    return {
      publishedUrl: formUrl,
      editUrl: editUrl
    };
  } else {
    Logger.log('Активна форма не знайдена');
    return {
      error: 'Активна форма не знайдена'
    };
  }
}