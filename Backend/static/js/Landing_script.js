document.addEventListener("DOMContentLoaded", () => {
  // Mobile Menu Toggle
  const mobileMenuBtn = document.querySelector(".mobile-menu-btn")
  const nav = document.querySelector("nav")

  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener("click", function () {
      this.classList.toggle("active")
      nav.classList.toggle("active")
    })
  }

  // Header Scroll Effect
  const header = document.querySelector("header")

  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      header.classList.add("scrolled")
    } else {
      header.classList.remove("scrolled")
    }
  })

  // Floating UI Animation
  const floatingUI = document.querySelector(".floating-ui")

  if (floatingUI) {
    document.addEventListener("mousemove", (e) => {
      const x = e.clientX / window.innerWidth
      const y = e.clientY / window.innerHeight

      floatingUI.style.transform = `translate(${x * 20 - 10}px, ${y * 20 - 10}px)`
    })
  }

  // Parallax Scrolling Effect
  const parallaxElements = document.querySelectorAll(".step-image")

  window.addEventListener("scroll", () => {
    parallaxElements.forEach((element) => {
      const position = element.getBoundingClientRect()
      const scrollPosition = position.top / window.innerHeight

      if (position.top < window.innerHeight && position.bottom > 0) {
        element.querySelector(".step-img").style.transform = `translateY(${scrollPosition * 50}px)`
      }
    })
  })

  // Scroll Animation for Steps
  const steps = document.querySelectorAll(".step")

  function checkSteps() {
    steps.forEach((step) => {
      const position = step.getBoundingClientRect()

      // If the step is in the viewport
      if (position.top < window.innerHeight * 0.8 && position.bottom > 0) {
        step.classList.add("active")
      } else {
        step.classList.remove("active")
      }
    })
  }

  window.addEventListener("scroll", checkSteps)
  checkSteps() // Check on load

  // Testimonial Slider
  const testimonials = document.querySelectorAll(".testimonial")
  const dots = document.querySelectorAll(".dot")
  const prevBtn = document.querySelector(".prev-btn")
  const nextBtn = document.querySelector(".next-btn")
  let currentSlide = 0

  function showSlide(index) {
    testimonials.forEach((testimonial) => testimonial.classList.remove("active"))
    dots.forEach((dot) => dot.classList.remove("active"))

    testimonials[index].classList.add("active")
    dots[index].classList.add("active")
    currentSlide = index
  }

  if (prevBtn && nextBtn) {
    prevBtn.addEventListener("click", () => {
      currentSlide = (currentSlide - 1 + testimonials.length) % testimonials.length
      showSlide(currentSlide)
    })

    nextBtn.addEventListener("click", () => {
      currentSlide = (currentSlide + 1) % testimonials.length
      showSlide(currentSlide)
    })
  }

  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      showSlide(index)
    })
  })

  // Auto slide for testimonials
  setInterval(() => {
    if (document.hasFocus()) {
      currentSlide = (currentSlide + 1) % testimonials.length
      showSlide(currentSlide)
    }
  }, 5000)

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()

      const targetId = this.getAttribute("href")
      if (targetId === "#") return

      const targetElement = document.querySelector(targetId)
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80,
          behavior: "smooth",
        })
      }
    })
  })

  // Hover effects for feature cards
  const featureCards = document.querySelectorAll(".feature-card")

  featureCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-10px)"
      this.style.boxShadow = "0 15px 40px rgba(0, 0, 0, 0.3)"
    })

    card.addEventListener("mouseleave", function () {
      this.style.transform = ""
      this.style.boxShadow = ""
    })
  })

  // Animated CTA button glow effect
  const ctaButtons = document.querySelectorAll(".cta-button")

  ctaButtons.forEach((button) => {
    button.addEventListener("mouseenter", function () {
      this.querySelector(".button-glow").style.opacity = "1"
    })

    button.addEventListener("mouseleave", function () {
      this.querySelector(".button-glow").style.opacity = "0"
    })
  })

  // Pricing card hover effect
  const pricingCards = document.querySelectorAll(".pricing-card")

  pricingCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      if (!this.classList.contains("featured")) {
        this.style.transform = "translateY(-10px)"
      } else {
        this.style.transform = "scale(1.08)"
      }
    })

    card.addEventListener("mouseleave", function () {
      if (!this.classList.contains("featured")) {
        this.style.transform = ""
      } else {
        this.style.transform = "scale(1.05)"
      }
    })
  })

  // Form submission prevention
  const forms = document.querySelectorAll("form")

  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      const button = this.querySelector('button[type="submit"]')
      const originalText = button.textContent

      button.textContent = "Submitted!"
      button.style.background = "#00c16e"

      setTimeout(() => {
        button.textContent = originalText
        button.style.background = ""
        this.reset()
      }, 2000)
    })
  })

  // Initialize animations on page load
  showSlide(0)
})

