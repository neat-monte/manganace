<template>
  <div class="introduction">
    <div class="title">Introduction</div>
    <p>
      You are invited to participate in a research project which is being
      conducted by a bachelor's student at Radboud University. The procedure
      involves looking at human face images and moving a slider, which will take
      <i>approximately</i> <strong>30 minutes</strong>. Your participation in
      this research study is voluntary and you may withdraw at any time.
      <strong>The data collected will be made fully anonymous.</strong>
    </p>
    <div class="title">Instructions</div>
    <p>
      You will be provided with a single emotion, a slider and an image of a
      person. By moving the slider to the right, the mentioned emotion will be
      applied stronger on the displayed face. On the other hand, by moving the
      slider to the left, the emotion will be reduced. The task is to place the
      slider where you think the provided emotion looks most natural on the
      person's face.
    </p>
    <p>
      Should you want more information on the research project, please feel free
      to contact the student at
      <strong>m.makelis@student.ru.nl</strong>
    </p>
  </div>
</template>

<script>
export default {
  name: "Introduction",
};
</script>

<style lang="scss" scoped>
.introduction {
  p {
    text-align: justify;
  }
}
</style>