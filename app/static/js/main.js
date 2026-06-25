function checkQuiz() {
  const input = document.getElementById('quiz-input');
  const answerEl = document.getElementById('quiz-answer-data');
  const feedback = document.getElementById('quiz-feedback');

  if (!input || !answerEl || !feedback) return;

  const userAnswer = input.value.trim().toLowerCase();
  const correctAnswer = answerEl.dataset.answer.trim().toLowerCase();

  feedback.style.display = 'block';

  if (!userAnswer) {
    feedback.className = 'quiz-feedback quiz-feedback--incorrect';
    feedback.textContent = 'Please type an answer first.';
    return;
  }

  // Accept answer if user input is contained in the correct answer or matches closely
  const isCorrect = correctAnswer === userAnswer
    || correctAnswer.includes(userAnswer)
    || userAnswer.includes(correctAnswer);

  if (isCorrect) {
    feedback.className = 'quiz-feedback quiz-feedback--correct';
    feedback.textContent = 'Correct! Well done.';
  } else {
    feedback.className = 'quiz-feedback quiz-feedback--incorrect';
    feedback.textContent = 'Not quite. The answer is: ' + answerEl.dataset.answer;
  }
}

// Allow pressing Enter in the quiz input to submit
document.addEventListener('DOMContentLoaded', function () {
  const quizInput = document.getElementById('quiz-input');
  if (quizInput) {
    quizInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') checkQuiz();
    });
  }

  // Scroll sidebar to highlight active topic
  const activeTopicLink = document.querySelector('.sidebar-topics .topic-item.active');
  if (activeTopicLink) {
    activeTopicLink.scrollIntoView({ block: 'nearest' });
  }

  // Theme toggle — flip the data-theme attribute and remember the choice.
  // The anti-flash script in <head> reads this value on the next page load.
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      const root = document.documentElement;
      const goingDark = root.getAttribute('data-theme') !== 'dark';
      if (goingDark) {
        root.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
      } else {
        root.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
      }
    });
  }
});
