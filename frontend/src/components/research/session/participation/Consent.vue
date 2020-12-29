<template>
  <div class="consent">
    <div class="title">Informed consent</div>
    <h3>General Information (version 2.1, April 2020)</h3>
    <p>
      This study is part of the research of the DondersCentre of Cognition
      (DCC). This centre is part of the Donders Institute, Radboud University
      Nijmegen. For our research we need volunteers to participate in various
      experiments, e.g. language, perception, action or memory tasks
    </p>
    <h3>Ethical approval</h3>
    <p>
      Each study you may participate in has been reviewed and approved by an
      independent ethics committee (the
      <a
        href="https://www.ru.nl/socialsciences/research/ethics-committee-social-science-ecss/"
        target="_blank"
      >
        Ethics Committee of Faculty of Social Sciences, Radboud University
        Nijmegen </a
      >)
    </p>
    <h3>Risks benefits and confidentiality</h3>
    <p>
      All our research and research methods have negligible to minimal risks.
      Although you will not benefit from this study personally, we hope that the
      results will contribute to scientific knowledge about behaviour. In this
      study we won’t collect personal identifiable data, hence all of your
      responses will be collected and processed anonymously. Demographic data or
      data concerning health, background or preferences, that are not
      identifying, may be collected for scientific purposes.
    </p>
    <h3>Information about the experiment and giving consent</h3>
    <p>
      It is recommended to read this information carefully, before you give
      consent. Consent is provided by ticking the checkbox at the bottom. You
      have the right to withdraw from the study at any time without giving a
      reason.
    </p>
    <h3>Payment</h3>
    <p>
      Students of Radboud University can be awarded with credit points. For 1
      hour of participation 1 credit point will be granted. Credit point
      allocation occurs via the SONA system. Other potential subjects
      participating in this study won’t receive a reimbursement.
    </p>
    <h3>Use and preservation of your data</h3>
    <p>
      Your research data is stored and archived on protected servers on the
      Radboud University Nijmegen for at least 10 years. When this experiment is
      finalized and a report or article is written on this, the concomitant
      experimental data are shared or made public, enabling verification, re-use
      and/or replication of these research results. Your data will be protected
      according tothe European law (European General Data Protection Regulation
      (GDPR)).
    </p>
    <h3>After participation</h3>
    <p>
      We appreciate hearing about your experiences as a participant. You can
      give your feedback - with or without personal information - via this
      <a
        href="https://www.ru.nl/donders/forms/feedback-webform-dcc-en/"
        target="_blank"
      >
        webform </a
      >. In case of questions or complaints about an experiment or about
      payment, contact the responsible experimenter first. You can also contact
      an independent contact person who is not involved in the study
      (independent contact person: Miriam Kos, of the Donders Centre for
      Cognition (dcclabcoordinator@socsci.ru.nl; tel 0243612650)) or fill out
      the above mentioned webform. If applicable the independent contact person
      will contact you by email or phone.
    </p>

    <p>
      <strong>
        By ticking on the box "I give my consent to take part in this
        experiment",
      </strong>
    </p>
    <p>I confirm that:</p>
    <ul>
      <li>
        I was satisfactorily informed about the study in writing, by means of
        the general information, version 2.1, April 2020.
      </li>
      <li>I have carefully considered participation in the experiment.</li>
      <li>I participate voluntarily.</li>
    </ul>
    <p>I agree that:</p>
    <ul>
      <li>
        My research data will be acquired and stored anonymously for scientific
        purposes until 10 years after the research has been finalized.
      </li>
      <li>
        Demographic data or data concerning my health, background or preferences
        is collected for scientific purposes.
      </li>
      <li>
        My not directly identifiable research data will be made public for
        verification, re-use and/or replication.
      </li>
    </ul>
    <p>I understand that:</p>
    <ul>
      <li>
        I have the right to withdraw from the experiment without having to give
        a reason.
      </li>
      <li>
        My privacy is protected according to applicable European law (European
        General Data Protection Regulation (GDPR)).
      </li>
      <li>
        My consent will be sought every time I participate in a new experiment.
      </li>
    </ul>
    <a-checkbox
      class="consent-box"
      :checked="consent"
      @change="$emit('update:consent', $event.target.checked)"
    >
      <strong>I give my consent to take part in this experiment</strong>
    </a-checkbox>
    <p class="date">{{ moment().format("DD-MM-YYYY") }}</p>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "Consent",

  props: {
    consent: Boolean,
  },

  setup() {
    return { moment };
  },
};
</script>

<style lang="scss" scoped>
.consent {
  p,
  ul,
  h3 {
    text-align: left;
  }

  .consent-box {
    margin: 20px 0;
  }

  .date {
    text-align: center;
  }
}
</style>