<script setup>
const faqs = ref([
  {
    question: 'How do I use the Stock Analyser?',
    answer: 'Enter a stock symbol in the search box and click "Go!" to see detailed technical analysis including Ichimoku, Candlestick patterns, and various indicators.'
  },
  {
    question: 'What is Changed Now?',
    answer: 'Changed Now shows real-time stock movements based on various technical indicators like RSI, Fibonacci Pivots, Camarilla Pivots, ADX, and Ichimoku.'
  },
  {
    question: 'How do I connect my broker?',
    answer: 'Go to "Connect Your Broker" page and select your broker from the list. Follow the authentication steps to link your trading account.'
  },
  {
    question: 'What are the different timeframes available?',
    answer: 'We offer Intraday, Daily, Weekly, and Monthly timeframes for analysis. You can switch between them using the tabs on each analysis page.'
  },
  {
    question: 'How do I interpret Bullish and Bearish signals?',
    answer: 'Green chips/indicators represent bullish (buy) signals while red represents bearish (sell) signals. Always use multiple indicators for confirmation.'
  },
])

const supportEmail = ref('')
const supportMessage = ref('')
const supportSubject = ref('')

const submitSupport = () => {
  console.log('Support request submitted:', {
    email: supportEmail.value,
    subject: supportSubject.value,
    message: supportMessage.value
  })
  supportEmail.value = ''
  supportSubject.value = ''
  supportMessage.value = ''
}
</script>

<template>
  <div class="ask-help-page">
    <!-- Page Header -->
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h4 class="text-h4 font-weight-bold">Ask Help</h4>
        <VBreadcrumbs :items="[{ title: 'Home', to: '/' }, { title: 'Ask Help', disabled: true }]" class="pa-0" />
      </div>
    </div>

    <VRow>
      <!-- FAQs -->
      <VCol cols="12" md="7">
        <VCard>
          <VCardTitle>Frequently Asked Questions</VCardTitle>
          <VCardText>
            <VExpansionPanels>
              <VExpansionPanel
                v-for="(faq, index) in faqs"
                :key="index"
                :title="faq.question"
              >
                <template #text>
                  {{ faq.answer }}
                </template>
              </VExpansionPanel>
            </VExpansionPanels>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Contact Support -->
      <VCol cols="12" md="5">
        <VCard>
          <VCardTitle>Contact Support</VCardTitle>
          <VCardText>
            <VForm @submit.prevent="submitSupport">
              <VTextField
                v-model="supportEmail"
                label="Email"
                type="email"
                required
                class="mb-3"
              />
              <VTextField
                v-model="supportSubject"
                label="Subject"
                required
                class="mb-3"
              />
              <VTextarea
                v-model="supportMessage"
                label="Message"
                rows="4"
                required
                class="mb-3"
              />
              <VBtn type="submit" color="primary" block>
                Submit Request
              </VBtn>
            </VForm>
          </VCardText>
        </VCard>

        <!-- Quick Links -->
        <VCard class="mt-4">
          <VCardTitle>Quick Links</VCardTitle>
          <VCardText>
            <VList>
              <VListItem href="https://neotrader.in/video-tutorials/" target="_blank">
                <template #prepend>
                  <VIcon icon="tabler-video" />
                </template>
                <VListItemTitle>Video Tutorials</VListItemTitle>
              </VListItem>
              <VListItem href="https://training.neotrader.in" target="_blank">
                <template #prepend>
                  <VIcon icon="tabler-school" />
                </template>
                <VListItemTitle>Training Portal</VListItemTitle>
              </VListItem>
              <VListItem href="https://t.me/+K85HU-yNmT9hYjFl" target="_blank">
                <template #prepend>
                  <VIcon icon="tabler-brand-telegram" />
                </template>
                <VListItemTitle>Telegram Support</VListItemTitle>
              </VListItem>
            </VList>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </div>
</template>
