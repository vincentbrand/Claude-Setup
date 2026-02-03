---
name: vue3-dev
description: Apply vue development standards, Vue 3 frontend. Use when working on Vue codebase or similar projects.
user-invocable: true
---


## When to Use
Claude applies this skill when:
- Building Vue 3 components with Composition API
- Implementing frontend features
- Writing tests with Playwright
- Managing application state with Pinia
- Setting up routing with Vue Router

## Architecture Overview

### Frontend Stack
- Vue 3 with Composition API (`<script setup>`)
- Tailwind CSS for utility-first styling
- Scoped SCSS for component-specific styles
- Pinia for state management
- Vue Router for navigation
- Minimal, clean design aesthetic

## Coding Standards

### Vue 3 Components
```vue
<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  title: String,
  items: Array
})

const isActive = ref(false)
const filteredItems = computed(() => {
  return props.items.filter(item => item.visible)
})

const handleClick = () => {
  isActive.value = !isActive.value
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <h1 class="text-2xl font-semibold">{{ title }}</h1>
    <button 
      @click="handleClick"
      class="px-4 py-2 bg-blue-600 text-white rounded"
    >
      Toggle
    </button>
  </div>
</template>

<style scoped lang="scss">
.custom-component {
  &__header {
    padding: 1rem;
    background: linear-gradient(to right, #667eea, #764ba2);
  }

  &__content {
    margin-top: 1rem;
  }
}
</style>
```


## State Management with Pinia

### Store Definition
```javascript
// stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  
  const isAuthenticated = computed(() => !!user.value)
  
  async function login(credentials) {
    // API call
    const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    })
    const data = await response.json()
    
    user.value = data.user
    token.value = data.token
    localStorage.setItem('token', data.token)
  }
  
  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }
  
  return {
    user,
    token,
    isAuthenticated,
    login,
    logout
  }
})
```

### Using Stores in Components
```vue
<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
}
</script>
```

### JavaScript Conventions
- Use `const` and `let`, avoid `var`
- Use arrow functions for consistency
- Destructure props and objects
- Keep functions small and focused
- Write lean, readable code

### Styling Guidelines
- Use Tailwind utility classes for layout and common styles
- Use scoped SCSS for component-specific styling
- Minimal, clean aesthetic
- Consistent spacing and typography
- Responsive design by default
- Use BEM naming convention in SCSS when needed



### Lean Code Principles
- Keep components focused and single-purpose
- Extract reusable logic into composables
- Avoid deep nesting
- Use early returns to reduce complexity
- Write self-documenting code with clear variable names

### State Management
- Use Pinia for global state
- Keep store modules focused and small
- Use composables for shared logic

## Code Organization
```
src/
├── api/            # API connections files
├── assets/         # Assets
├── components/     # Reusable Vue components
├── composables/    # Composition API utilities
├── directives/     # Directives
├── layouts/        # Layout components
├── locales/        # All language l18n related files
├── router/         # Vue router files
├── services/       # Services files
├── stores/         # Pinia stores
├── utils/          # Helper functions
└── views/          # Page components
```

## Design System
- Clean, minimal aesthetic
- Professional appearance
- Smooth transitions and interactions
- Consistent color palette and typography
- Responsive layouts using Tailwind breakpoints


## Best Practices
- Write lean, consistent code
- Keep components small and focused
- Use composition API with `<script setup>`
- Leverage Tailwind for rapid styling
- Use scoped SCSS for complex component styles
- Manage global state with Pinia
- Handle navigation with Vue Router
- Test critical user flows with Playwright