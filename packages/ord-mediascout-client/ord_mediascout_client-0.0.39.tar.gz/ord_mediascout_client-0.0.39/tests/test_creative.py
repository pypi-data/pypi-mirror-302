import pytest

from ord_mediascout_client import (
    CampaignType,
    CreateCreativeMediaDataItem,
    CreateCreativeRequest,
    CreativeForm,
    CreativeStatus,
    CreativeTextDataItemWebApiDto,
    EditCreativeRequest,
    GetCreativesWebApiDto,
)
from ord_mediascout_client.models import FileType


@pytest.fixture
def create_mediadata_creative(client):
    request_data = CreateCreativeRequest(
        finalContractId='CTiwhIpoQ_F0OEPpKj8vWKGg',
        initialContractId='CTKLAzsvgYREmK0unGXLsCTg',
        type=CampaignType.CPM,
        form=CreativeForm.Banner,
        advertiserUrls=['https://clisite1.ru/', 'https://clisite2.ru/'],
        description='Test mediadata creative 333',
        targetAudienceParams=[],
        isSelfPromotion=False,
        isNative=False,
        isSocial=False,
        mediaData=[
            CreateCreativeMediaDataItem(
                fileName='logo.svg',
                fileType=FileType.Image,
                # fileContentBase64="string",
                srcUrl='https://kokoc.com/local/templates/kokoc/web/images/logo/logo.svg',
                description='Тестовый баннер 333',
                isArchive=False,
            )
        ],
    )

    response_data = client.create_creative(request_data)
    # print(f"{response_data=}")
    response_data.mediaData[0] = request_data.mediaData[0]
    # print(f"{response_data=}")
    return response_data


def test_create_mediadata_creative(create_mediadata_creative):
    assert create_mediadata_creative is not None


#     request_data = CreateCreativeRequest(
#         finalContractId='CTiwhIpoQ_F0OEPpKj8vWKGg',
#         initialContractId='CTKLAzsvgYREmK0unGXLsCTg',
#         type=CampaignType.CPM,
#         form=CreativeForm.Banner,
#         advertiserUrls=['https://clisite1.ru/', 'https://clisite2.ru/'],
#         description='Test mediadata creative 333',
#         targetAudienceParams=[],
#         isSelfPromotion=False,
#         isNative=False,
#         isSocial=False,
#         mediaData=[
#             CreateCreativeMediaDataItem(
#                 fileName='logo.svg',
#                 fileType=FileType.Image,
#                 # fileContentBase64="string",
#                 srcUrl='https://kokoc.com/local/templates/kokoc/web/images/logo/logo.svg',
#                 description='Тестовый баннер 333',
#                 isArchive=False,
#             )
#         ],
#     )
#
#     response_data = client.create_creative(request_data)
#
#     assert response_data.id is not None
#     return response_data


def test_create_textdata_creative(client):
    request_data = CreateCreativeRequest(
        finalContractId='CTiwhIpoQ_F0OEPpKj8vWKGg',
        initialContractId='CTKLAzsvgYREmK0unGXLsCTg',
        type=CampaignType.CPM,
        form=CreativeForm.Text,
        advertiserUrls=['https://clisite1.ru/', 'https://clisite2.ru/'],
        description='Test textdata creative 555',
        targetAudienceParams=[],
        isSelfPromotion=False,
        isNative=False,
        isSocial=False,
        textData=[CreativeTextDataItemWebApiDto(textData='Creative 555 text data test')],
    )

    response_data = client.create_creative(request_data)

    assert response_data.id is not None


def test_get_creatives(client):
    request_data = GetCreativesWebApiDto(status=CreativeStatus.Active)

    response_data = client.get_creatives(request_data)

    for creative in response_data:
        assert creative.id is not None


def test_edit_creative(client, create_mediadata_creative):
    # print(f"{create_mediadata_creative=}")
    # print(f"{create_mediadata_creative.id=}")
    create_mediadata_creative.nativeCustomerId = 12345
    # print(f"VARS: {vars(create_mediadata_creative)}")
    data = vars(create_mediadata_creative)
    data.pop('creativeGroupName', None)
    data.pop('creativeGroupName', None)
    data.pop('creativeGroupStartDate', None)
    data.pop('creativeGroupEndDate', None)
    data['advertiserUrls'] = ['https://clisite1.ru/', 'https://clisite2.ru/']
    request_data = EditCreativeRequest(**data)
    # print(f"{request_data=}")
    client.edit_creative(request_data)
    # print(f"{response_data=}")
