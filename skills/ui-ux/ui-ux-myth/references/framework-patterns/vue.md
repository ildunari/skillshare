# Vue patterns (UI implementation)

Use this when implementing in Vue 3 (Composition API).

## 1) Component organization

Suggested structure:

```
src/
  components/
    ui/          # primitives
    layout/      # layout primitives
    features/    # domain components
  styles/
    tokens.css
    base.css
```

## 2) SFC baseline

- Keep template semantic.
- Keep styles token-driven.
- Keep script logic focused.

```vue
<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  title: string;
  subtitle?: string;
  loading?: boolean;
}>();

const hasSubtitle = computed(() => Boolean(props.subtitle));
</script>

<template>
  <section class="Section">
    <header class="SectionHeader">
      <h2 class="Title">{{ title }}</h2>
      <p v-if="hasSubtitle" class="Subtitle">{{ subtitle }}</p>
    </header>

    <div class="Body">
      <slot />
    </div>
  </section>
</template>

<style scoped>
.Section { padding-block: clamp(2.5rem, 4vw, 4rem); }
.Title { font-size: clamp(1.8rem, 3vw, 2.6rem); }
.Subtitle { color: var(--muted); }
</style>
```

## 3) Accessibility patterns

- Use real `<button>` and `<a>` elements.
- For icon-only buttons, provide `aria-label`.

```vue
<template>
  <button type="button" class="IconButton" :aria-label="label">
    <slot />
  </button>
</template>

<script setup lang="ts">
defineProps<{ label: string }>();
</script>
```

## 4) Dialogs + Teleport

For modals/dialogs:
- teleport to body
- trap focus (use a library if possible)
- close on Esc
- restore focus

```vue
<template>
  <Teleport to="body">
    <div v-if="open" class="Overlay" @keydown.esc="close">
      <div
        class="Dialog"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="titleId"
      >
        <h2 :id="titleId">{{ title }}</h2>
        <slot />
        <button type="button" @click="close">Close</button>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useId } from "vue";

const props = defineProps<{ open: boolean; title: string }>();
const emit = defineEmits<{ (e: "close"): void }>();

const titleId = useId();
const close = () => emit("close");
</script>
```

Note: You still need focus trapping; this snippet shows semantics and structure.

## 5) Transitions

Use Vue `<Transition>` for simple reveal/hide.
See: [../animations.md](../animations.md)
