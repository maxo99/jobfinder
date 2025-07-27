# CHANGELOG


## v0.12.0 (2025-07-27)

### Bug Fixes

- Reloading of stats
  ([`adcf984`](https://github.com/maxo99/jobfinder/commit/adcf984a5ac8c242baeb7a5c6e88393bd8deeeb2))

### Features

- Updates to sidebar and navigation logic
  ([`b247b10`](https://github.com/maxo99/jobfinder/commit/b247b1096fabf9dfc37fd0de23eadf2e38501bee))

- Updates to stats display
  ([`4c56294`](https://github.com/maxo99/jobfinder/commit/4c56294811331115cf9c2289caa73c5ee290e86f))

### Refactoring

- Class moving and cleanup
  ([`1caf57b`](https://github.com/maxo99/jobfinder/commit/1caf57bb6ce70685d0f5d6433eadfaefa6e9af8d))

- Using page links instead of tabs for navigation
  ([`4deddcf`](https://github.com/maxo99/jobfinder/commit/4deddcfc402d45e6e0e0191e8eb4dfcd7f1b469f))

### Testing

- Readding app layer test
  ([`2f2201b`](https://github.com/maxo99/jobfinder/commit/2f2201bb8a866e786da93258e780eb899b0b1f4c))

- Updates to testes to incorporate both similarity searches
  ([`8bc8df9`](https://github.com/maxo99/jobfinder/commit/8bc8df931be7e2271aaad15c096081cff86c43fc))


## v0.11.0 (2025-07-25)

### Features

- Introduction of embedding and search logic
  ([`4f61a9b`](https://github.com/maxo99/jobfinder/commit/4f61a9b336599594ee9e1ef56ffac128a617067a))

### Refactoring

- Refactor data management and main page structure
  ([`7f68964`](https://github.com/maxo99/jobfinder/commit/7f68964d2d1be9e8a14b9225d7763f412fb8241c))


## v0.10.0 (2025-07-24)

### Build System

- Changing build-system to uv_build
  ([`3937033`](https://github.com/maxo99/jobfinder/commit/3937033a6878675765fd59ff5b18d61ff660545a))

### Features

- Updates to chat call using a json schema to ensure response validation
  ([`11298b8`](https://github.com/maxo99/jobfinder/commit/11298b83569624b847e0601d7fc9fb0560a1e29f))

### Testing

- Updates to test data for mocks
  ([`ab7ae7e`](https://github.com/maxo99/jobfinder/commit/ab7ae7e5c537c49cd487a040abfb0f74a1fff93e))

- Updates to test data for mocks
  ([`fc68cb1`](https://github.com/maxo99/jobfinder/commit/fc68cb1449228dd167c899d796eb0fc670da6cd2))

- Updates to test setup for mocks
  ([`f0bdf63`](https://github.com/maxo99/jobfinder/commit/f0bdf63230f9271201456f3cf9ffce9672744f84))

- Updates to test setup for mocks
  ([`f93bdb9`](https://github.com/maxo99/jobfinder/commit/f93bdb958ee3cdf3e1224c6f4d2a83cc8a487d15))

- Updating local test setup/teardown via pytest-docker
  ([`a473e5a`](https://github.com/maxo99/jobfinder/commit/a473e5ab3372486f779f7b28f22025a11c847fbd))


## v0.9.2 (2025-07-21)

### Bug Fixes

- Updating scoring and displaying of qualifications
  ([`ff22ae7`](https://github.com/maxo99/jobfinder/commit/ff22ae7e91c86c8acc47d67cbd826cb5e0f836db))

### Chores

- Consolidating formating/linting to the toml + updating copilot default instructions
  ([`4d79b6c`](https://github.com/maxo99/jobfinder/commit/4d79b6ca7d749672bba0d8015313bf172b6d4685))

- Fixing local testing configuration so that coverage does not block debugger
  ([`0df5362`](https://github.com/maxo99/jobfinder/commit/0df53629e52c7263bc4ec6c7b062383c1120bbfd))

- Updating settings and lock file
  ([`0165427`](https://github.com/maxo99/jobfinder/commit/0165427fdb55253ac5fc2418ceb4ef53390fae61))

- Vscode settings updates for pylint and debugpy
  ([`7d0e795`](https://github.com/maxo99/jobfinder/commit/7d0e79500172cbf6a4083791a98e4a574daaf8d9))

### Continuous Integration

- Updating pytest comment action
  ([`f24cf33`](https://github.com/maxo99/jobfinder/commit/f24cf33a3947b6f9a7dfe3f73c72124d6f9c7efb))

- Using cached uv for faster actions
  ([`ca9fff8`](https://github.com/maxo99/jobfinder/commit/ca9fff832a8acf274ac0ced397034ee3e41071e7))

### Documentation

- Adding badges to readme
  ([`aa51e30`](https://github.com/maxo99/jobfinder/commit/aa51e30d561ca4c6a57b0cf1251cb7ed638eca0c))

- Update to readme and refactoring roadmap and walkthrough to separate document
  ([`1d93206`](https://github.com/maxo99/jobfinder/commit/1d932067cd42c4cd3dabd1f45b561e5ade253013))

- Updating readme
  ([`f8aabc5`](https://github.com/maxo99/jobfinder/commit/f8aabc5b860706b52e5a47e6c5be72e9e122b166))

### Refactoring

- Using common methods where appropriate
  ([`565ad7d`](https://github.com/maxo99/jobfinder/commit/565ad7dd1c668bff5dd1b0f0bc675acb21c88af1))

- **pgvector**: Updates for postgres docker support
  ([`3b96463`](https://github.com/maxo99/jobfinder/commit/3b96463a56df40dc94013f7c610c9d8746e12e36))

### Testing

- Adding wait for docker compose postgres to be ready
  ([`f1a716b`](https://github.com/maxo99/jobfinder/commit/f1a716b3a93ce377e6f457d2ad6f2cec95da9c2e))

- Adding wait for docker compose postgres to be ready
  ([`2d4b357`](https://github.com/maxo99/jobfinder/commit/2d4b357e414a23ea7ab398a1226c96e28c352d75))

- Including mock chat response
  ([`edcb40f`](https://github.com/maxo99/jobfinder/commit/edcb40fd22ae6bccda505040b817b19f83958cab))

- Including mock chat response
  ([`8fd846f`](https://github.com/maxo99/jobfinder/commit/8fd846f56377bab33eea143f2463c9ec7b69da21))

- Updates after refactor
  ([`c97202e`](https://github.com/maxo99/jobfinder/commit/c97202e16e03eeb9e44c4adb9c56e6d17abf0d10))

- Updating ci runner
  ([`684eda1`](https://github.com/maxo99/jobfinder/commit/684eda1c1e5d1a9db2f3b87b6438fff69c690835))

- Updating ci runner
  ([`04232c0`](https://github.com/maxo99/jobfinder/commit/04232c0f031fe7f5d9c7baad3dc908b112e0bfe3))

- Updating CI tests for docker compose mocked ollama
  ([`95a9453`](https://github.com/maxo99/jobfinder/commit/95a94530df771835b31564e02c5d4d582edb875d))

- Updating mockserver initializer
  ([`139b2bc`](https://github.com/maxo99/jobfinder/commit/139b2bcde0398e6b90dcaf9c46ee9e8c6a6c723a))

- Updating mockserver initializer for embed api
  ([`b4accd2`](https://github.com/maxo99/jobfinder/commit/b4accd2699356bd6fb63857228e3b14e0ab78c9b))

- Updating pytest docker compose shutdown
  ([`f760a72`](https://github.com/maxo99/jobfinder/commit/f760a72cfe79450758e3e64256aaa3604dbceaef))


## v0.9.1 (2025-07-13)

### Bug Fixes

- Update to cicd for release validation
  ([`055c988`](https://github.com/maxo99/jobfinder/commit/055c9882aa9c6adf207c79a60672f152714175e5))

### Continuous Integration

- Coverage badge population fix
  ([`c978029`](https://github.com/maxo99/jobfinder/commit/c978029033ade05613a77f22f7cac07790b747ba))

- Updating pytest action
  ([`d846833`](https://github.com/maxo99/jobfinder/commit/d84683309d76ff51861a3da17ef5a9fb4fc3458c))

- Updating release workflow to only trigger after succesful tests
  ([`88b1d93`](https://github.com/maxo99/jobfinder/commit/88b1d9315bb5b1aa89dcbf6eb49d877f4595506e))

### Documentation

- Update README.md
  ([`7d35c3f`](https://github.com/maxo99/jobfinder/commit/7d35c3f0ea6a4fd01ee603ae3c7e9bb602e2650a))


## v0.9.0 (2025-07-13)

### Build System

- Introducing docker and docker compose builds and deployments
  ([`e347802`](https://github.com/maxo99/jobfinder/commit/e3478022cb357bde4460a8b0e826efaa387ae575))

- Moving watchtower to streamlit-cloud only builds
  ([`1f921c6`](https://github.com/maxo99/jobfinder/commit/1f921c600ca787b31f208e3906b41dfbd4523b08))

### Continuous Integration

- Adding pytest coverage gh action
  ([`b798715`](https://github.com/maxo99/jobfinder/commit/b7987151a365b2a2279cfc4c4242da444a8f582a))

- Settings and coverage badge cleanup
  ([`67d2b3f`](https://github.com/maxo99/jobfinder/commit/67d2b3f2f6eed0cfc31532ae4328fce819a84a2a))

- Settings and coverage badge cleanup
  ([`3e912dd`](https://github.com/maxo99/jobfinder/commit/3e912dd8cd65436947c7747ad1257c042fb2082b))

### Features

- **elasticsearch**: Adding elasticsearch to docker compose and introducing code for client
  implementation
  ([`7a68de2`](https://github.com/maxo99/jobfinder/commit/7a68de2c5ef0cd06a3ec9a54e85552786a65cae2))

### Refactoring

- Adding backend instance and updating session management to better facilitate testing
  ([`b61c6e7`](https://github.com/maxo99/jobfinder/commit/b61c6e7bbfb6c223d42ce56f112adc6a33077c59))

- Moving filters to sidebar so that can apply to all dataframes within current rendering
  ([`a4f1315`](https://github.com/maxo99/jobfinder/commit/a4f1315cf1b5c71df44fb97fada1e51eda68eb07))

### Testing

- Including summarization test
  ([`f523139`](https://github.com/maxo99/jobfinder/commit/f523139b8ffb52301d4ae1dfdfe7f097077bc92a))

- Testing github badge for coverage results
  ([`a077b6c`](https://github.com/maxo99/jobfinder/commit/a077b6cd90a22d00fea45213b71fe28e299f0f59))

- Updates to adapter tests for mocking external resources
  ([`ea91dbd`](https://github.com/maxo99/jobfinder/commit/ea91dbd3b1584e57354960ec97761c364084c941))

- Updating elastisearch client tests
  ([`a237057`](https://github.com/maxo99/jobfinder/commit/a237057938c38e50219fe4bc8af2f8598f17a362))

- Updating pytest action to add coverage to readme
  ([`8cff062`](https://github.com/maxo99/jobfinder/commit/8cff062174ac4759476dfd8d03353750b708388b))

- Using pytest-docker for integration tests
  ([`6e6f7d1`](https://github.com/maxo99/jobfinder/commit/6e6f7d1e260ae6c3b52834b13938594d3faaecac))


## v0.8.0 (2025-07-08)

### Chores

- Updating vscode settings
  ([`933b867`](https://github.com/maxo99/jobfinder/commit/933b867a34bc42a19807635a79b6bbb0cfed705e))

### Documentation

- Updating readme with sequence diagram
  ([`efb22c3`](https://github.com/maxo99/jobfinder/commit/efb22c385663a3554f3331ba196364568af93f4f))

### Features

- Incorporating AI summarization for jobs
  ([`4030f66`](https://github.com/maxo99/jobfinder/commit/4030f66ec2af13cd6aa8a1f9403417411c6a1cfa))

### Refactoring

- Application restructuring for better session import
  ([`69d926c`](https://github.com/maxo99/jobfinder/commit/69d926c1bdea028ae5a199f81b11ecd737a52916))

- Moving tab organization
  ([`af19be5`](https://github.com/maxo99/jobfinder/commit/af19be5d4c781869e65454faec059c2c4b2e696a))

- Using datafilter object
  ([`61b8a0a`](https://github.com/maxo99/jobfinder/commit/61b8a0af8dfec113683b8744678b7581f3c3d455))


## v0.7.0 (2025-07-07)


## v0.6.1 (2025-07-07)

### Bug Fixes

- Proper filtering of excludeds + lint cleanups
  ([`910eb1a`](https://github.com/maxo99/jobfinder/commit/910eb1a8cc15aa1795a9d2e743af5d0f89ba6125))

### Features

- Including summarize jobs usertype
  ([`2522ba3`](https://github.com/maxo99/jobfinder/commit/2522ba32fc3744bb03633f71cbd1f887158a840e))

- Storing job pulls as raw data to enable reloading without additional scraping calls + moving add
  record to separate tab
  ([`91d686c`](https://github.com/maxo99/jobfinder/commit/91d686c59c72f2ff51ac8f9124a8cfec42cf0dd2))

### Refactoring

- Moving add record to separate tab
  ([`a13c97d`](https://github.com/maxo99/jobfinder/commit/a13c97db335a9820b4246d3d52b5e3e314c71cd7))


## v0.6.0 (2025-06-30)

### Features

- **logging**: Inclusion of watchtower for posting logs to cloudwatch
  ([`2e10ce2`](https://github.com/maxo99/jobfinder/commit/2e10ce2a2ed6ec66cb6cfadaa9135b5b1506fd51))


## v0.5.0 (2025-06-30)


## v0.4.0 (2025-06-30)

### Chores

- Using gitkeep for data dir
  ([`8f704c8`](https://github.com/maxo99/jobfinder/commit/8f704c89fbdbeef0c501814f3dd0e160c984e636))

### Documentation

- Adding configuration of chat model to readme
  ([`def729b`](https://github.com/maxo99/jobfinder/commit/def729b82873592295f0e239730f3672f99d5a9a))

### Features

- Adding exclusions to job pulling for is_remote & job_type
  ([`353ff63`](https://github.com/maxo99/jobfinder/commit/353ff6351d356de952a46f48f0d520b472e0a4f4))

- Inclusion of field classifier to track who scored + modified column for last edit + fixes to
  loading in individual job details page
  ([`3c2bbc8`](https://github.com/maxo99/jobfinder/commit/3c2bbc836c9b16f57f8c9573dff37c5f85a4f40d))


## v0.3.0 (2025-06-29)

### Bug Fixes

- **prompt**: Adding missing validation method
  ([`cd6dae2`](https://github.com/maxo99/jobfinder/commit/cd6dae2a60a88c96b0b5828c245633b0d5fb516d))

### Code Style

- Updating display organization and including version in footer
  ([`20bc2d4`](https://github.com/maxo99/jobfinder/commit/20bc2d4be744cb77ad51b27d04a90caa5854db65))

### Features

- **prompt**: Cleanup
  ([`d7195dd`](https://github.com/maxo99/jobfinder/commit/d7195ddb6731d840ea2fb6b5627af2debc073873))

- **prompt**: Implementing prompt construction for automated scoring handled by OpenAI completions
  ([`3c43a21`](https://github.com/maxo99/jobfinder/commit/3c43a21a503b086e9aff0582f224b95240bbd132))

- **prompt**: Initial input
  ([`6c2fb10`](https://github.com/maxo99/jobfinder/commit/6c2fb10509b5a76f88afd2bd81405ddafa340463))

- **prompt**: Organization
  ([`6c2e6d4`](https://github.com/maxo99/jobfinder/commit/6c2e6d49ffe5f8460a35af617b48e706b3f8c4a5))

- **prompt**: Organization
  ([`449eed9`](https://github.com/maxo99/jobfinder/commit/449eed997e185ffd586b32b87a7aa3ad0ebe2a46))

- **prompt**: Rework progress
  ([`c9ec28a`](https://github.com/maxo99/jobfinder/commit/c9ec28ada9400fbe77251782af9df3c9197ecd50))

- **prompt**: Scoring util page
  ([`2141b41`](https://github.com/maxo99/jobfinder/commit/2141b4135248d8ed976b553413e9fdd0a3a777e3))

- **prompt**: Structure and organization
  ([`92bb920`](https://github.com/maxo99/jobfinder/commit/92bb920ef6cca776485784ea6d411c7046434c58))

- **prompt**: Style
  ([`2636e8f`](https://github.com/maxo99/jobfinder/commit/2636e8f07b7ae9903eeecc98a24a58a84d083483))

- **prompt**: Templating logic
  ([`21879a3`](https://github.com/maxo99/jobfinder/commit/21879a3c63a9abab55b5e43868d74d525b36a0d1))


## v0.2.1 (2025-06-27)

### Bug Fixes

- **stats**: Reintegrating statistics and updates to listings display
  ([`b2217f3`](https://github.com/maxo99/jobfinder/commit/b2217f33e34e45a6a44236d1eee89f916706c6e6))

### Chores

- Adding MIT License
  ([`abd98c4`](https://github.com/maxo99/jobfinder/commit/abd98c437ee43aca74f9984caf1b19b027f1613a))

- Adding VSCode launch config for debugging
  ([`371217c`](https://github.com/maxo99/jobfinder/commit/371217c3a7f092e736dd8cfc0e829804d91cd9b5))


## v0.2.0 (2025-06-27)

### Chores

- Including vscode debug configuration for streamlit
  ([`4d0ffe3`](https://github.com/maxo99/jobfinder/commit/4d0ffe3f1fd154f86990131c26fd9336b303cea2))


## v0.1.2 (2025-06-26)

### Bug Fixes

- Displaying of first entry before any have been selected
  ([`2641639`](https://github.com/maxo99/jobfinder/commit/26416391baed6e0ca9febb3ae6847a7c9f34f023))

### Chores

- Updating version in python definition
  ([`fc8154e`](https://github.com/maxo99/jobfinder/commit/fc8154e96ead22c6cd94bfaf443cc32c7c41e6a8))

### Documentation

- Updating readme with purpose
  ([`1da8de6`](https://github.com/maxo99/jobfinder/commit/1da8de6451aea397a735cdc08d684acf496967c0))

### Features

- **listings**: Support for bulk operations to update data of filtered listings
  ([`d6329b9`](https://github.com/maxo99/jobfinder/commit/d6329b93a1e03bad4df14a931d0f4c885bf3c99f))


## v0.1.1 (2025-06-26)

### Bug Fixes

- Initial release setting
  ([`fdda017`](https://github.com/maxo99/jobfinder/commit/fdda017f3a584237d6a06ab63f93e0408538dc31))

- Long description display
  ([`68d3763`](https://github.com/maxo99/jobfinder/commit/68d3763aa6e911a50f929854648e132f9e1c8037))

- Uploading release upon build
  ([`85ca5f3`](https://github.com/maxo99/jobfinder/commit/85ca5f3d7b1ee4639cf8b429981c4f40c6fecb3e))

- Using python-semantic-release_publish-action
  ([`3eabe60`](https://github.com/maxo99/jobfinder/commit/3eabe60d25858aa0f4da058c0419201c53ac0756))


## v0.1.0 (2025-06-26)

### Bug Fixes

- Release format
  ([`57e06c8`](https://github.com/maxo99/jobfinder/commit/57e06c808e3bcd484127453442ba1c2231034b1d))

- Release versioning
  ([`52cf63d`](https://github.com/maxo99/jobfinder/commit/52cf63d6e0d2a30d582d5dad28d3dc9d85200cec))

- Semantic release action
  ([`1c82cf2`](https://github.com/maxo99/jobfinder/commit/1c82cf283e6b1683449fea869adcd651b7f3b36d))

- Semantic release adding of initial tag
  ([`49dd0f3`](https://github.com/maxo99/jobfinder/commit/49dd0f3d55336a7c0d7999d1638d89dfd30d2b87))

- Semantic release initial version
  ([`8e35bf3`](https://github.com/maxo99/jobfinder/commit/8e35bf3d0010bf439c981931c84b94eebc2cb2b4))

- Setting of initial version
  ([`e6114c3`](https://github.com/maxo99/jobfinder/commit/e6114c3b911cf319c6577ba20baab790cb28c059))

- Updating changelog util for future compatibility
  ([`dcaf845`](https://github.com/maxo99/jobfinder/commit/dcaf8452c26b3ba4a7137d06307f0d52de596dd3))

- Updating semantic release action
  ([`fb47600`](https://github.com/maxo99/jobfinder/commit/fb4760082a96a16849e13d0ef32a7da73b36af50))

- Version setting
  ([`7cc3a96`](https://github.com/maxo99/jobfinder/commit/7cc3a96e8ac53fc9306637f57e34869d8a15f1a9))

- **clear-data**: Removing confirmation check which was breaking funcationality
  ([`7c4c2b1`](https://github.com/maxo99/jobfinder/commit/7c4c2b1e1146db18a363da02825e8c62f7f7b4d1))

- **merge**: Resolving duplicate main method
  ([`c81c256`](https://github.com/maxo99/jobfinder/commit/c81c256ad5357939f90a672d34821c5ea20e430f))

### Build System

- **uv**: Configuring uv to call streamlit
  ([`50b7af1`](https://github.com/maxo99/jobfinder/commit/50b7af11bc61a35ebc6d823b2b951548c5379ae1))

- **uv**: Initializing as uv project
  ([`039234c`](https://github.com/maxo99/jobfinder/commit/039234cfeeb075f71a8de09a3f6d0f08d82a51aa))

### Continuous Integration

- **semantic**: Adding semantic versioning for release management
  ([`bbb1903`](https://github.com/maxo99/jobfinder/commit/bbb1903414d733545a3a1675eae86c89f7ef57ed))

### Features

- Release versioning
  ([`9e3aff3`](https://github.com/maxo99/jobfinder/commit/9e3aff3dc17a62ee63e3776ad04704eaeea8cfce))

- **generation**: Initial logic generation
  ([`a4e417d`](https://github.com/maxo99/jobfinder/commit/a4e417d501e58ea45e39f3520122706663397eb2))

- **init**: Documentation initialization
  ([`6197d37`](https://github.com/maxo99/jobfinder/commit/6197d37e4941e66682ca1b1d594e9c76ba8b5a11))

- **logger**: Adding basic logger implementation
  ([`11c891c`](https://github.com/maxo99/jobfinder/commit/11c891c537856090a57c1896d653e19e53accee5))

- **model**: Datamodel conversion helpers and testing + details displayment updates
  ([`a83dd8d`](https://github.com/maxo99/jobfinder/commit/a83dd8d500806280a443835d35deae23f3cf6d95))

- **model**: Inclusion and updates to generated pydantic model
  ([`127b3b5`](https://github.com/maxo99/jobfinder/commit/127b3b56ea8dc48c1fde16d4bd61a1241a8badd8))

- **persistence**: Updating data dir logic
  ([`dd7a137`](https://github.com/maxo99/jobfinder/commit/dd7a137d2961643270320320a57052cf2b831e26))

- **scoring**: Replaceing 'notes' for 'pros','cons','score' columns
  ([`f72be2d`](https://github.com/maxo99/jobfinder/commit/f72be2d8b6098a1722c469b6a7859e30f1c844e7))

- **stats**: Updating stats display
  ([`2e28640`](https://github.com/maxo99/jobfinder/commit/2e28640443e3911d84d882657b81438ed3562f2e))

- **status**: Updated business logic from 'viewed' -> 'status' which defaults to 'new' then 'viewed'
  once modified, along with 'excluded' which will be leveradged for next features
  ([`8b720e1`](https://github.com/maxo99/jobfinder/commit/8b720e10c39e358e0e96de0c6df87f252924f091))

### Refactoring

- Split of listings overview logic
  ([`1a63c66`](https://github.com/maxo99/jobfinder/commit/1a63c66fdff03effa6178dbdaee995205a7cdc41))

- Updates to datamodel and individual job details view
  ([`9e54e8d`](https://github.com/maxo99/jobfinder/commit/9e54e8d817344786424a6c921e37f6a69c4b5794))

- **modularize**: Logic separation
  ([`efdca77`](https://github.com/maxo99/jobfinder/commit/efdca77e34ba741ed304bba04dc399405d90c35b))

### Testing

- Including model loading and validation test before updates
  ([`ed4298b`](https://github.com/maxo99/jobfinder/commit/ed4298b33aeeabd356214c67e87be118f70f4726))
