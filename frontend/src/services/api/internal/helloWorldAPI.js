import Client from './client';

export default {
  async getHelloWorldMessage() {
    return Client.get('/hello/api/v1/ping')
      .then((response) => JSON.stringify(response.data.hello))
      .catch((error) => {
        // Error
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          // eslint-disable-next-line
          console.log('The request was made and the server responded with a status code != 2xx', error.response);
        } else if (error.request) {
          // The request was made but no response was received
          // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
          // eslint-disable-next-line
          console.log('The request was made but no response was received', error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          // eslint-disable-next-line
          console.log('Something happened in setting up the request that triggered an Error', error.message);
        }

        // In our hello world example, we simply want to display the error in the view
        throw error;
      });
  },
};
