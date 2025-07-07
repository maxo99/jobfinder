# CHANGELOG


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
