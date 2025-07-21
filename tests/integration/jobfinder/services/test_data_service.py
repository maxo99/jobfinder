import time


def test_populate_index(fix_dataservice, jobs_testdata):
    fix_dataservice.store_jobs(jobs_testdata)
    time.sleep(2)

    populated_count = len(fix_dataservice.get_jobs())
    assert populated_count >= len(jobs_testdata)


# def test_updating_summary(
#     fix_dataservice,
#     jobs_testdata
# ):
#     _test_id = "FAKE_JOB_ID"
#     _test_qualifications = [
#         {"skill": "Python", "requirement": "required", "experience": "5 years"},
#         {"skill": "SQL", "requirement": "preferred", "experience": "2+ years"},
#     ]

#     test_data = jobs_testdata.copy()[0:1]
#     test_data[0].id = _test_id
#     fix_dataservice.store_jobs(test_data)
#     time.sleep(0.5)
#     returned_job = fix_dataservice.get_by_id(_test_id)
#     assert returned_job is not None
#     assert returned_job.id == _test_id
#     assert returned_job.qualifications == []
#     test_data = test_data.copy()
#     test_data[0].qualifications = [Qualifications(**q) for q in _test_qualifications]
#     fix_dataservice.store_jobs(test_data)
#     time.sleep(0.5)
#     updated_job = fix_dataservice.get_by_id(_test_id)
#     assert updated_job is not None
#     assert updated_job.id == _test_id
#     assert updated_job.qualifications == _test_qualifications

# def test_populate_with_vectors(
#     fix_dataservice,
#     raw_jobs_df
# ):
#     _raw_jobs = load_raw_jobs()

#     _input_data = load_data2(state="processed").copy()
#     _starting_count = len(_input_data)
#     for doc in _input_data.to_dict(orient="records"):
#         job = Job.from_dict(doc)
#     time.sleep(2)
#     response = fix_elasticsearchclient.client.count(index=test_index)
#     print(f"Indexed {response['count']} documents with vectors in index '{test_index}'.")
#     assert response["count"] == len(test_data), (
#         "Not all documents with vectors were indexed correctly."
#     )
