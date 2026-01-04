<script setup>
import AuthProvider from '@/views/pages/authentication/AuthProvider.vue'
import { useGenerateImageVariant } from '@core/composable/useGenerateImageVariant'
import authV2RegisterIllustrationBorderedDark from '@images/pages/auth-v2-register-illustration-bordered-dark.png'
import authV2RegisterIllustrationBorderedLight from '@images/pages/auth-v2-register-illustration-bordered-light.png'
import authV2RegisterIllustrationDark from '@images/pages/auth-v2-register-illustration-dark.png'
import authV2RegisterIllustrationLight from '@images/pages/auth-v2-register-illustration-light.png'
import authV2MaskDark from '@images/pages/misc-mask-dark.png'
import authV2MaskLight from '@images/pages/misc-mask-light.png'
import { VNodeRenderer } from '@layouts/components/VNodeRenderer'
import { themeConfig } from '@themeConfig'

definePage({ meta: { layout: 'blank' } })

const router = useRouter()

const form = ref({
  email: '',
  phone: '',
  status: '',
  password: '',
  confirmPassword: '',
  privacyPolicies: false,
})

const isPasswordVisible = ref(false)
const isConfirmPasswordVisible = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const statusOptions = [
  'Trader',
  'Investor',
  'Analyst',
  'Beginner',
  'Professional',
]

const passwordRules = computed(() => ({
  minLength: form.value.password.length >= 8,
  hasUppercase: /[A-Z]/.test(form.value.password),
  hasLowercase: /[a-z]/.test(form.value.password),
  hasNumber: /[0-9]/.test(form.value.password),
  hasSpecial: /[!@#$%^&*(),.?":{}|<>]/.test(form.value.password),
}))

const isPasswordValid = computed(() => {
  return Object.values(passwordRules.value).every(rule => rule)
})

const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!form.value.email || !form.value.phone || !form.value.status || !form.value.password || !form.value.confirmPassword) {
    errorMessage.value = 'All fields are required'
    return
  }

  if (!isPasswordValid.value) {
    errorMessage.value = 'Please meet all password requirements'
    return
  }

  if (form.value.password !== form.value.confirmPassword) {
    errorMessage.value = 'Passwords do not match'
    return
  }

  if (!form.value.privacyPolicies) {
    errorMessage.value = 'You must agree to the Terms of Use and Privacy Policy'
    return
  }

  isLoading.value = true

  try {
    const response = await fetch('/api/auth/register.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: form.value.email,
        phone: form.value.phone,
        status: form.value.status,
        password: form.value.password,
        confirm_password: form.value.confirmPassword,
      }),
    })

    const data = await response.json()

    if (data.success) {
      successMessage.value = data.message
      setTimeout(() => {
        router.push('/login')
      }, 2000)
    } else {
      errorMessage.value = data.message
    }
  } catch (error) {
    errorMessage.value = 'Network error. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const authThemeImg = useGenerateImageVariant(authV2RegisterIllustrationLight, authV2RegisterIllustrationDark, authV2RegisterIllustrationBorderedLight, authV2RegisterIllustrationBorderedDark, true)
const authThemeMask = useGenerateImageVariant(authV2MaskLight, authV2MaskDark)
</script>

<template>
  <RouterLink to="/">
    <div class="auth-logo d-flex align-center gap-x-3">
      <VNodeRenderer :nodes="themeConfig.app.logo" />
      <h1 class="auth-title">
        {{ themeConfig.app.title }}
      </h1>
    </div>
  </RouterLink>

  <VRow
    no-gutters
    class="auth-wrapper bg-surface"
  >
    <VCol
      md="8"
      class="d-none d-md-flex"
    >
      <div class="position-relative bg-background w-100 me-0">
        <div
          class="d-flex align-center justify-center w-100 h-100"
          style="padding-inline: 6.25rem;"
        >
          <VImg
            max-width="613"
            :src="authThemeImg"
            class="auth-illustration mt-16 mb-2"
          />
        </div>

        <img
          class="auth-footer-mask"
          :src="authThemeMask"
          alt="auth-footer-mask"
          height="280"
          width="100"
        >
      </div>
    </VCol>

    <VCol
      cols="12"
      md="4"
      class="auth-card-v2 d-flex align-center justify-center"
    >
      <VCard
        flat
        :max-width="500"
        class="mt-12 mt-sm-0 pa-4"
      >
        <VCardText>
          <h4 class="text-h4 mb-1">
            Sign Up
          </h4>
          <p class="mb-0">
            Create your account and start trading
          </p>
        </VCardText>

        <VCardText v-if="errorMessage">
          <VAlert
            color="error"
            variant="tonal"
          >
            {{ errorMessage }}
          </VAlert>
        </VCardText>

        <VCardText v-if="successMessage">
          <VAlert
            color="success"
            variant="tonal"
          >
            {{ successMessage }}
          </VAlert>
        </VCardText>

        <VCardText>
          <VForm @submit.prevent="handleRegister">
            <VRow>
              <!-- email -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.email"
                  autofocus
                  label="Email"
                  type="email"
                  placeholder="Enter your email"
                />
              </VCol>

              <!-- phone -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.phone"
                  label="Phone Number"
                  type="tel"
                  placeholder="Enter your phone number"
                />
              </VCol>

              <!-- status select -->
              <VCol cols="12">
                <AppSelect
                  v-model="form.status"
                  label="Select a status"
                  :items="statusOptions"
                  placeholder="Select a status"
                />
              </VCol>

              <!-- password -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.password"
                  label="Password"
                  placeholder="············"
                  :type="isPasswordVisible ? 'text' : 'password'"
                  :append-inner-icon="isPasswordVisible ? 'tabler-eye-off' : 'tabler-eye'"
                  @click:append-inner="isPasswordVisible = !isPasswordVisible"
                />

                <!-- Password requirements -->
                <div class="mt-2">
                  <div
                    class="text-caption"
                    :class="passwordRules.minLength ? 'text-success' : 'text-disabled'"
                  >
                    <VIcon
                      size="14"
                      :icon="passwordRules.minLength ? 'tabler-check' : 'tabler-circle'"
                    />
                    Must be at least 8 characters
                  </div>
                  <div
                    class="text-caption"
                    :class="passwordRules.hasUppercase && passwordRules.hasLowercase ? 'text-success' : 'text-disabled'"
                  >
                    <VIcon
                      size="14"
                      :icon="passwordRules.hasUppercase && passwordRules.hasLowercase ? 'tabler-check' : 'tabler-circle'"
                    />
                    Use uppercase and lowercase letters (e.g. Aa)
                  </div>
                  <div
                    class="text-caption"
                    :class="passwordRules.hasNumber ? 'text-success' : 'text-disabled'"
                  >
                    <VIcon
                      size="14"
                      :icon="passwordRules.hasNumber ? 'tabler-check' : 'tabler-circle'"
                    />
                    Use a number (e.g. 1234)
                  </div>
                  <div
                    class="text-caption"
                    :class="passwordRules.hasSpecial ? 'text-success' : 'text-disabled'"
                  >
                    <VIcon
                      size="14"
                      :icon="passwordRules.hasSpecial ? 'tabler-check' : 'tabler-circle'"
                    />
                    Use a special character (e.g. @!$%)
                  </div>
                </div>
              </VCol>

              <!-- confirm password -->
              <VCol cols="12">
                <AppTextField
                  v-model="form.confirmPassword"
                  label="Confirm Password"
                  placeholder="············"
                  :type="isConfirmPasswordVisible ? 'text' : 'password'"
                  :append-inner-icon="isConfirmPasswordVisible ? 'tabler-eye-off' : 'tabler-eye'"
                  @click:append-inner="isConfirmPasswordVisible = !isConfirmPasswordVisible"
                />
              </VCol>

              <!-- privacy policy -->
              <VCol cols="12">
                <VCheckbox v-model="form.privacyPolicies">
                  <template #label>
                    <span class="text-body-2">
                      By signing up, I confirm that I am 18 years of age or older, and I agree to the
                      <a
                        href="#"
                        class="text-primary"
                      >Terms of Use</a>
                      and
                      <a
                        href="#"
                        class="text-primary"
                      >Privacy Policy</a>.
                    </span>
                  </template>
                </VCheckbox>
              </VCol>

              <VCol cols="12">
                <VBtn
                  block
                  type="submit"
                  :loading="isLoading"
                  :disabled="isLoading"
                >
                  Sign Up
                </VBtn>
              </VCol>

              <!-- login link -->
              <VCol
                cols="12"
                class="text-center"
              >
                <span>Already have an account?</span>
                <RouterLink
                  class="text-primary ms-2"
                  to="/login"
                >
                  Login here!
                </RouterLink>
              </VCol>

              <VCol
                cols="12"
                class="d-flex align-center"
              >
                <VDivider />
                <span class="mx-4">or</span>
                <VDivider />
              </VCol>

              <!-- auth providers -->
              <VCol
                cols="12"
                class="text-center"
              >
                <AuthProvider />
              </VCol>
            </VRow>
          </VForm>
        </VCardText>
      </VCard>
    </VCol>
  </VRow>
</template>

<style lang="scss">
@use "@core/scss/template/pages/page-auth.scss";
</style>
