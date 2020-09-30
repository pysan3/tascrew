<template>
  <div class="container-fluid">
    <header>
      <h4 class="display-4 mb-4 text-center">November 2017</h4>
      <div class="row d-none d-sm-flex p-1 bg-dark text-white">
        <h5 class="col-sm p-1 text-center">Sunday</h5>
        <h5 class="col-sm p-1 text-center">Monday</h5>
        <h5 class="col-sm p-1 text-center">Tuesday</h5>
        <h5 class="col-sm p-1 text-center">Wednesday</h5>
        <h5 class="col-sm p-1 text-center">Thursday</h5>
        <h5 class="col-sm p-1 text-center">Friday</h5>
        <h5 class="col-sm p-1 text-center">Saturday</h5>
      </div>
    </header>
    <div class="row border border-right-0 border-bottom-0">
      <div class="day col-sm p-2 border border-left-0 border-top-0 text-truncate d-none d-sm-inline-block bg-light text-muted">
        <h5 class="row align-items-center">
          <span class="date col-1">29</span>
          <small class="col d-sm-none text-center text-muted">Sunday</small>
          <span class="col-1"></span>
        </h5>
        <p class="d-sm-none">No events</p>
      </div>
      <div class="day col-sm p-2 border border-left-0 border-top-0 text-truncate d-none d-sm-inline-block bg-light text-muted">
        <h5 class="row align-items-center">
          <span class="date col-1">30</span>
          <small class="col d-sm-none text-center text-muted">Monday</small>
          <span class="col-1"></span>
        </h5>
        <p class="d-sm-none">No events</p>
      </div>
      <div class="day col-sm p-2 border border-left-0 border-top-0 text-truncate d-none d-sm-inline-block bg-light text-muted">
        <h5 class="row align-items-center">
          <span class="date col-1">31</span>
          <small class="col d-sm-none text-center text-muted">Tuesday</small>
          <span class="col-1"></span>
        </h5>
        <p class="d-sm-none">No events</p>
      </div>
      <div class="day col-sm p-2 border border-left-0 border-top-0 text-truncate ">
        <h5 class="row align-items-center">
          <span class="date col-1">1</span>
          <small class="col d-sm-none text-center text-muted">Wednesday</small>
          <span class="col-1"></span>
        </h5>
        <p class="d-sm-none">No events</p>
      </div>
      <div class="day col-sm p-2 border border-left-0 border-top-0 text-truncate ">
        <h5 class="row align-items-center">
          <span class="date col-1">2</span>
          <small class="col d-sm-none text-center text-muted">Thursday</small>
          <span class="col-1"></span>
        </h5>
        <p class="d-sm-none">No events</p>
      </div>
      <div class="day col-sm p-2 border border-left-0 border-top-0 text-truncate ">
        <h5 class="row align-items-center">
          <span class="date col-1">3</span>
          <small class="col d-sm-none text-center text-muted">Friday</small>
          <span class="col-1"></span>
        </h5>
        <a class="event d-block p-1 pl-2 pr-2 mb-1 rounded text-truncate small bg-info text-white" title="Test Event 1">Test Event 1</a>
      </div>
      <div class="day col-sm p-2 border border-left-0 border-top-0 text-truncate ">
        <h5 class="row align-items-center">
          <span class="date col-1">4</span>
          <small class="col d-sm-none text-center text-muted">Saturday</small>
          <span class="col-1"></span>
        </h5>
        <p class="d-sm-none">No events</p>
      </div>
      <div class="w-100"></div>
      <div class="day col-sm p-2 border border-left-0 border-top-0 text-truncate ">
        <h5 class="row align-items-center">
          <span class="date col-1">5</span>
          <small class="col d-sm-none text-center text-muted">Sunday</small>
          <span class="col-1"></span>
        </h5>
        <p class="d-sm-none">No events</p>
      </div>
    </div>
  </div>
</template>

<script>
// get calendar data with this.$router.params.id
</script>

<style scoped>
@media (max-width:575px) {
  .display-4 {
    font-size: 1.5rem;
  }
  .day h5 {
    background-color: #f8f9fa;
    padding: 3px 5px 5px;
    margin: -8px -8px 8px -8px;
  }
  .date {
    padding-left: 4px;
  }
}

@media (min-width: 576px) {
  .day {
    height: 14.2857vw;
  }
}
</style>
